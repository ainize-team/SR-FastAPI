from typing import Dict

from pydantic import BaseModel

from enums import ModelEnum


class ModelInfoModel(BaseModel):
    file_name: str
    model_url: str
    sha_256: str
    scale: int


MODEL_INFO: Dict[ModelEnum, ModelInfoModel] = {
    ModelEnum.SWIN_LR_X2: ModelInfoModel(
        file_name="003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x2_GAN.pth",
        model_url="https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x2_GAN.pth",
        sha_256="f397408977a3e07eb06afb7238d453a12ef35ebab7328a54241f307860dbe342",
        scale=2,
    ),
    ModelEnum.SWIN_LR_X4: ModelInfoModel(
        file_name="003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth",
        model_url="https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth",
        sha_256="b9afb61e65e04eb7f8aba5095d070bbe9af28df76acd0c9405aeb33b814bcfc6",
        scale=4,
    ),
    ModelEnum.SWIN_LR_LARGE_X4: ModelInfoModel(
        file_name="003_realSR_BSRGAN_DFOWMFC_s64w8_SwinIR-L_x4_GAN.pth",
        model_url="https://github.com/JingyunLiang/SwinIR/releases/download/v0.0/003_realSR_BSRGAN_DFOWMFC_s64w8_SwinIR-L_x4_GAN.pth",
        sha_256="99adfa91350a84c99e946c1eb3d8fce34bc28f57d807b09dc8fe40a316328c0a",
        scale=4,
    ),
}
