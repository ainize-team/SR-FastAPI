from typing import Optional

from pydantic import BaseModel, HttpUrl

from enums import ResponseStatusEnum


class AsyncTaskResponse(BaseModel):
    task_id: str
    updated_at: int


class SuperResolutionWorkerOutput(BaseModel):
    input: str
    output: str


class Images(BaseModel):
    input: HttpUrl
    output: Optional[HttpUrl]


class Error(BaseModel):
    status_code: int
    error_message: str


class InitSuperResolutionData(BaseModel):
    user_id: str
    images: Images
    status: ResponseStatusEnum = ResponseStatusEnum.PENDING
    error: Optional[Error] = None
    updated_at: int = 0


class SuperResolutionResponse(BaseModel):
    output: Optional[HttpUrl]
    status: ResponseStatusEnum = ResponseStatusEnum.PENDING
    updated_at: int = 0
