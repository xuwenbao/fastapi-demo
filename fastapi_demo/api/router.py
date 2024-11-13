from fastapi import APIRouter

from fastapi_demo.api.v1 import diocese_router

router = APIRouter(prefix='/api/v1', )
router.include_router(diocese_router)