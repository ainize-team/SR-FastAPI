import torch
from pydantic import BaseSettings

from constants import MODEL_INFO
from enums import DeviceEnum, EnvEnum, ModelEnum


class ServerSettings(BaseSettings):
    app_name: str = "Super Resolution Fast API Server"
    app_version: str = "0.1.0"
    app_env: EnvEnum = EnvEnum.DEV


class ModelSettings(BaseSettings):
    device: DeviceEnum = DeviceEnum.CUDA if torch.cuda.is_available() else DeviceEnum.CPU
    model_name: ModelEnum = ModelEnum.SWIN_LR_LARGE_X4
    model_path: str = f"./model/{MODEL_INFO[ModelEnum.SWIN_LR_LARGE_X4].file_name}"


class FirebaseSettings(BaseSettings):
    firebase_app_name: str = "super-resolution"
    cred_path: str = "./key/serviceAccountKey.json"
    database_url: str
    storage_bucket: str


server_settings = ServerSettings()
model_settings = ModelSettings()
firebase_settings = FirebaseSettings()
