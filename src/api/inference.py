import os
import shutil
import uuid

from fastapi import APIRouter, HTTPException, Request, UploadFile, status
from firebase_admin import db

from enums import ResponseStatusEnum
from schemas import AsyncTaskResponse, Images, InitSuperResolutionData, SuperResolutionResponse
from settings import firebase_settings
from utils import get_now_timestamp, save_image_to_storage


router = APIRouter()


@router.post("/upscale", response_model=AsyncTaskResponse)
async def post_generation(request: Request, file: UploadFile):
    now = get_now_timestamp()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, str(now)))
    if file.content_type == "image/png":
        input_path = f"{task_id}/input.png"
        os.makedirs(task_id, exist_ok=True)
        with open(input_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        input_url = save_image_to_storage(task_id, input_path)
        shutil.rmtree(task_id, ignore_errors=True)
    else:
        raise HTTPException(status_code=400, detail="Only Support PNG file")
    app_name = firebase_settings.firebase_app_name
    db.reference(f"{app_name}/{task_id}").set(
        InitSuperResolutionData(
            user_id="",
            images=Images(input=input_url),
            status=ResponseStatusEnum.PENDING,
            updated_at=get_now_timestamp(),
        ).dict()
    )

    try:
        celery = request.app.state.celery
        celery.send_task(
            name="upscale",
            kwargs={
                "task_id": task_id,
            },
            queue="sr",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Celery Error({task_id}): {e}")

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
