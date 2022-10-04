from pydantic import BaseSettings

from enums import EnvEnum


class ServerSettings(BaseSettings):
    app_name: str = "Super Resolution Fast API Server"
    app_version: str = "0.1.0"
    app_env: EnvEnum = EnvEnum.DEV


class CelerySettings(BaseSettings):
    broker_uri: str = "amqp://guest:guest@localhost:5672//"


class FirebaseSettings(BaseSettings):
    firebase_app_name: str = "super-resolution"
    cred_path: str = "./key/serviceAccountKey.json"
    database_url: str
    storage_bucket: str


server_settings = ServerSettings()
celery_settings = CelerySettings()
firebase_settings = FirebaseSettings()
