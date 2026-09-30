import logging
import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import make_url

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")


logger = logging.getLogger(__name__)



""" Создание подключения к БД """
engine = create_async_engine(DATABASE_URL, echo=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session



class Base(DeclarativeBase):
    pass


async def create_database():
    url = make_url(DATABASE_URL)

    db_name = url.database

    admin_url = url.set(database='postgres')

    admin_engine = create_async_engine(admin_url, isolation_level='AUTOCOMMIT')

    async with admin_engine.connect() as conn:
        try:

            query = await conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name},
            )


            if query.scalar() is None:

                safe_name = db_name.replace('"', '""')
                query = await conn.execute(
                    text(f'CREATE DATABASE "{safe_name}"') # только в таких запросах параметризация WHERE, VALUES, SET
                )

                logger.info('База данных %s создана', db_name)
            else:
                logger.info('База данных %s уже существует', db_name)

        finally:
            admin_engine.dispose()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info('База данных создана')


