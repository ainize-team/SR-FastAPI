from enum import Enum, IntEnum


class StrEnum(str, Enum):
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class EnvEnum(StrEnum):
    DEV: str = "dev"
    PROD: str = "prod"


class ModelEnum(StrEnum):
    SWIN_LR_X2: str = "SwinLR_X2"
    SWIN_LR_X4: str = "SwinLR_X4"
    SWIN_LR_LARGE_X2: str = "SwinLR-Large_X2"
    SWIN_LR_LARGE_X4: str = "SwinLR-Large_X4"


class DeviceEnum(StrEnum):
    CPU: str = "cpu"
    CUDA: str = "cuda"


class ExitCodeEnum(IntEnum):
    MODEL_DOWNLOAD_ERROR: int = 1
    MODEL_CHECKSUM_ERROR: int = 2
    INVALID_MODEL_NAME: int = 3


class ResponseStatusEnum(StrEnum):
    PENDING: str = "pending"
    ASSIGNED: str = "assigned"
    COMPLETED: str = "completed"
    ERROR: str = "error"
