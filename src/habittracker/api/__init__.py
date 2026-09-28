from fastapi import APIRouter

from habittracker.api.habits import router as habits_router

main_router = APIRouter()

main_router.include_router(habits_router)