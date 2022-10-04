from fastapi import APIRouter

from api import inference


router = APIRouter()
router.include_router(inference.router)
