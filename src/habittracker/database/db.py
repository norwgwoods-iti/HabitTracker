from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import psycopg



""" Создание подключения к БД """
engine = create_async_engine(
    "postgresql+psycopg://nd:postgres@localhost/habittracker",
    pool_pre_ping=True,
    echo=False,)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session



class Base(DeclarativeBase):
    pass
#
# """ Создание подключения к БД """
# engine = create_async_engine("sqlite+aiosqlite:///database/habits.db")  # ! не создает директорию
#
# new_session = async_sessionmaker(engine, expire_on_commit=False)
#
# async def get_session():
#     async with new_session() as session:
#         yield session
#
#
#
# class Base(DeclarativeBase):
#     pass