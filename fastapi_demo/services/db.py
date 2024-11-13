from typing import Callable, AsyncGenerator

from loguru import logger
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fastapi_demo.services.config import AppSettings, get_settings


def create_db_and_tables(get_settings: Callable[[], AppSettings]):
    logger.info("creating tables ...")
    
    settings: AppSettings = get_settings()

    # we'll turn off this verbose logging of queries in production:
    echo = settings.testing
    # 使用同步engine创建数据库
    engine = create_engine(
        settings.mysql.database_url.replace("mysql+aiomysql", "mysql+pymysql"), echo=echo
    )
    SQLModel.metadata.create_all(engine)

    # 使用异步engine进行数据库操作
    return create_async_engine(settings.mysql.database_url, echo=echo)

async_engine = create_db_and_tables(get_settings)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session