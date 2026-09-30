import contextlib

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from habittracker.api import main_router
from habittracker.database.db import create_tables

from src.habittracker.database.function import update_database

from src.habittracker.database.db import engine, new_session, Base, create_database



@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):

    scheduler = AsyncIOScheduler()

    scheduler.add_job(update_database, 'cron', hour=00, minute=00, args=[new_session])
    scheduler.start()

    await create_database()
    await create_tables()

    yield

    scheduler.shutdown(wait=True)

    await engine.dispose()


app = FastAPI(
    title="Habit Tracker",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы с любых адресов (удобно для локальной разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Разрешает все заголовки
)


app.include_router(main_router)