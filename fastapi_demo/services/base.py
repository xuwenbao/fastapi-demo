from typing import TypeVar, Optional, List

from fastapi import HTTPException
from sqlmodel import SQLModel, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=SQLModel)


class BaseService:

    model: SQLModel

    @classmethod
    async def create(cls, session: AsyncSession, instance: T) -> T:
        """创建数据库记录"""
        try:
            instance = cls.model.model_validate(instance)
            
            async with session.begin():
                session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance
        except IntegrityError:
            raise HTTPException(status_code=409, detail="The record is already exists")

    @classmethod
    async def get_by_id(cls, session: AsyncSession, instance_id: int) -> Optional[T]:
        """通过ID获取记录"""
        statement = select(cls.model).where(cls.model.id == instance_id)
        result = await session.execute(statement)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(status_code=404, detail="Record not found")
        return instance

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[T]:
        """获取所有记录"""
        statement = select(cls.model)
        result = await session.execute(statement)
        return result.scalars().all()

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, instance_id: int) -> bool:
        """删除数据库记录"""
        instance = await cls.get_by_id(session, instance_id)
        await session.delete(instance)
        await session.commit()
        return True