import os
from datetime import datetime

from firebase_admin import storage

from settings import firebase_settings


def get_now_timestamp() -> int:
    return int(datetime.utcnow().timestamp() * 1000)


def save_image_to_storage(task_id: str, image_path: str) -> str:
    app_name = firebase_settings.firebase_app_name
    bucket = storage.bucket()
    base_name = os.path.basename(image_path)

    blob = bucket.blob(f"{app_name}/results/{task_id}/{base_name}")
    blob.upload_from_filename(image_path)
    blob.make_public()

    url = blob.public_url

    return url
