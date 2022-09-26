import os
from typing import Callable

from fastapi import FastAPI
from loguru import logger

from constants import MODEL_INFO
from enums import ExitCodeEnum
from settings import model_settings
from utils import define_model, download_model, get_hash


def load_model(app: FastAPI) -> None:

    model_name = model_settings.model_name
    model_path = model_settings.model_path

    # if model path is not valid, try to download model from url
    if not os.path.exists(model_path) or not os.path.isfile(model_path):
        logger.warning(f"{model_path} is not valid path, try to download model")
        try:
            model_hash = download_model(MODEL_INFO[model_name].model_url, model_path)
        except Exception as e:
            logger.error(f"Error : {e}")
            exit(ExitCodeEnum.MODEL_DOWNLOAD_ERROR)
    else:
        model_hash = get_hash(model_path)
    logger.info("Check sha256 value")
    if model_hash != MODEL_INFO[model_name].sha_256:
        logger.error(f"Sha256 value({model_hash}) is not valid, try to download model")
        try:
            model_hash = download_model(MODEL_INFO[model_name].model_url, model_path)
        except Exception as e:
            logger.error(f"Error : {e}")
            exit(ExitCodeEnum.MODEL_DOWNLOAD_ERROR)
        if model_hash != MODEL_INFO[model_name].sha_256:
            logger.error(f"Sha256 value({model_hash}) is not valid.")
            exit(ExitCodeEnum.MODEL_CHECKSUM_ERROR)
    app.state.model = define_model(model_name, model_path)
    app.state.model.to(model_settings.device)
    logger.info("The model was successfully loaded.")


def start_app_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        load_model(app)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        del app.state.model

    return shutdown
