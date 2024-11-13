from typing import List

from loguru import logger
from fastapi import APIRouter, Depends

from fastapi_demo.services import get_session, DioceseService
from fastapi_demo.models.diocese import DioceseCreate, DioceseRead

router = APIRouter(tags=["diocese"])


@router.post("/dioceses/", response_model=DioceseRead)
async def create_diocese(diocese: DioceseCreate, session=Depends(get_session)):
    logger.info("Attempting to create Diocese")
    return await DioceseService.create(session, diocese)


@router.get("/dioceses/{diocese_id}", response_model=DioceseRead)
async def read_diocese(diocese_id: int, session=Depends(get_session)):
    return await DioceseService.get_by_id(session, diocese_id)


@router.delete("/dioceses/{diocese_id}")
async def delete_diocese(diocese_id: int, session=Depends(get_session)):
    await DioceseService.delete_by_id(session, diocese_id)
    return {"detail": f"Diocese with ID {diocese_id} was deleted"}


@router.get("/dioceses", response_model=List[DioceseRead])
async def list_dioceses(session=Depends(get_session)):
    return await DioceseService.get_all(session)