from typing import Callable

import firebase_admin
from celery import Celery
from fastapi import FastAPI
from firebase_admin import credentials
from loguru import logger

from settings import celery_settings, firebase_settings


def _setup_firebase() -> None:
    cred = credentials.Certificate(firebase_settings.cred_path)
    firebase_admin.initialize_app(
        cred,
        {"databaseURL": firebase_settings.database_url, "storageBucket": firebase_settings.storage_bucket},
    )


def _setup_celery(app: FastAPI) -> None:
    logger.info("Setup Celery")
    app.state.celery = Celery(broker=celery_settings.broker_uri)


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        _setup_firebase()
        _setup_celery(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        del app.state.celery

    return shutdown
