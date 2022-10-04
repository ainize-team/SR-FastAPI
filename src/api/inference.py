import os
import shutil
import uuid

import requests
from celery import Celery
from fastapi import APIRouter, HTTPException, Request, UploadFile, status
from firebase_admin import db
from pydantic import HttpUrl

from enums import ResponseStatusEnum
from schemas import AsyncTaskResponse, Images, InitSuperResolutionData, SuperResolutionResponse
from settings import firebase_settings
from utils import get_now_timestamp, save_image_to_storage


router = APIRouter()


async def process(image_path: str, task_id: str, celery: Celery) -> None:
    input_url = save_image_to_storage(task_id, image_path)
    shutil.rmtree(task_id, ignore_errors=True)
    app_name = firebase_settings.firebase_app_name
    try:
        db.reference(f"{app_name}/{task_id}").set(
            InitSuperResolutionData(
                user_id="",
                images=Images(input=input_url),
                status=ResponseStatusEnum.PENDING,
                updated_at=get_now_timestamp(),
            ).dict()
        )
    except Exception as e:
        raise Exception(f"FireBase Error : {e}")
    try:
        celery.send_task(
            name="upscale",
            kwargs={
                "task_id": task_id,
            },
            queue="sr",
        )
    except Exception as e:
        raise Exception(f"CeleryError : {e}")


@router.post("/upscale/img", response_model=AsyncTaskResponse)
async def post_generation(request: Request, file: UploadFile):
    now = get_now_timestamp()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    celery: Celery = request.app.state.celery
    if file.content_type == "image/png":
        input_path = f"{task_id}/input.png"
        os.makedirs(task_id, exist_ok=True)
        with open(input_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        try:
            process(input_path, task_id, celery)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server Error: {e}")
    else:
        raise HTTPException(status_code=400, detail="Only Support PNG file")
    return AsyncTaskResponse(task_id=task_id, updated_at=now)


@router.post("/upscale/url", response_model=AsyncTaskResponse)
async def post_generation_img_url(request: Request, url: HttpUrl):
    now = get_now_timestamp()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    celery: Celery = request.app.state.celery
    try:
        res = requests.get(url)
        if res.headers.get("content-type") == "image/png":
            input_path = f"{task_id}/input.png"
            os.makedirs(task_id, exist_ok=True)
            with open(input_path, "wb") as f:
                f.write(res.content)
            try:
                process(input_path, task_id, celery)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Server Error: {e}")
        else:
            raise HTTPException(status_code=400, detail="Only Support PNG file")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Image URL Error : {e}")
    return AsyncTaskResponse(task_id=task_id, updated_at=now)


@router.get("/result/{task_id}", response_model=SuperResolutionResponse)
async def get_result(task_id: str):
    try:
        app_name = firebase_settings.firebase_app_name
        ref = db.reference(f"{app_name}/{task_id}")
        data = ref.get()
        if data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Task ID({task_id}) not found")
        if data["status"] == ResponseStatusEnum.ERROR:
            raise HTTPException(status_code=data["error"]["status_code"], detail=data["error"]["error_message"])
        return SuperResolutionResponse(
            status=data["status"],
            updated_at=data["updated_at"],
            output=data["images"]["output"] if data["status"] == ResponseStatusEnum.COMPLETED else None,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"FireBaseError({task_id}): {e}")
