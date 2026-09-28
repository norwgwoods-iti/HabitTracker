from typing import Annotated
import logging

from fastapi import APIRouter, Query, HTTPException

from sqlalchemy import select, delete
from starlette import status

from habittracker.api.function import get_habit_function
from habittracker.database.db import engine, Base
from habittracker.api.dependencies import SessionDep
from habittracker.models.habits import HabitModel, CheckinHabitModel
from habittracker.schemas.habits import HabitAddSchema, HabitSchema, CheckinHabitSchema

from datetime import date

from sqlalchemy.exc import IntegrityError

router = APIRouter()

logger = logging.getLogger(__name__)

""" POST """
@router.post("/setup_database",
          tags=["Установка Базы Данных 💽"],
          summary="Установить БД")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info('База Данных деактивирована')
        await conn.run_sync(Base.metadata.create_all)
        logger.info('База данных создана')
    return {
        "ok": True,
    }


""" POST """
@router.post("/habits",
          tags=["Привычки 🚬"],
          summary='Добавить новую привычку')
async def post_habits(habit: HabitAddSchema, session: SessionDep):
    new_habit = HabitModel(
        name=habit.name,
        description=habit.description
    )
    session.add(new_habit)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Habit with name {habit.name} already exists'
        )


    return {
        "ok": True,
    }



""" GET """
@router.get("/habits",
         tags=["Привычки 🚬"],
         summary="Получить список всех привычек")
async def get_habits(session: SessionDep) -> list[HabitSchema]:
    # query = select(HabitModel)  # Создаем запрос
    # result = await session.execute(query)  # Отправляем запрос
    # habits = result.scalars().all()  # Получаем все запси

    habits = await session.scalars(select(HabitModel))

    return habits.all()



""" GET """
@router.get("/habits/{habit_id}",
          tags=["Привычки 🚬"],
         summary="Получить привычку по ID")
async def get_habits(habit_id: int, session: SessionDep) -> HabitSchema:

    habit = await get_habit_function(session=session, id=habit_id, model=HabitModel)

    return habit


""" GET Stats """
@router.get("/habits/{habit_id}/stats")
async def get_habits_stats(
        habit_id: int,
        date_from: date,
        date_to: date,
        session: SessionDep) -> list[CheckinHabitSchema]:


    query = select(CheckinHabitModel).where(
        CheckinHabitModel.id_habit == habit_id,
        CheckinHabitModel.checkins_date.between(date_from, date_to)
    )

    result = await session.execute(query)

    habits_with_date = result.scalars().all()

    return habits_with_date



""" UPDATE """
@router.put("/habits/{habit_id}",
          tags=["Привычки 🚬"],
         summary="Обновить данные привычки по ID")
async def update_habits(habit_id: int, habit_data: HabitAddSchema, session: SessionDep):

    habit = await get_habit_function(session=session, id=habit_id, model=HabitModel)

    habit.name = habit_data.name
    habit.description = habit_data.description

    await session.commit()
    await session.refresh(habit)

    return {
        "ok": True,
    }



""" POST Toggle """
@router.post("/habits/{habit_id}/checkins",
              include_in_schema=False)
async def toggle_habit(habit_id: int, session: SessionDep):

    habit = await get_habit_function(session=session, id=habit_id, model=HabitModel)

    habit.checking = not habit.checking

    if habit.checking:
        new_check = CheckinHabitModel(
            id_habit=habit.id,
            checkins_date=date.today()
        )

        session.add(new_check)
    else:

        query = delete(CheckinHabitModel).where(
            CheckinHabitModel.id_habit == habit.id,
            CheckinHabitModel.checkins_date == date.today()
        )

        await session.execute(query)

    await session.commit()
    await session.refresh(habit)



    return {
        "ok": True,
        "checking": habit.checking
    }



""" DELETE """
@router.delete("/habits/{habit_id}/checkins",
          tags=["Привычки 🚬"],
        summary="Удалить привычку по дате")
async def delete_habit_with_date(
        habit_id: int,
        date: Annotated[date, Query(
            alias='date'
        )],
        session: SessionDep
):
    # !!!!!!
    query = delete(CheckinHabitModel).where(
        CheckinHabitModel.id == habit_id,
        CheckinHabitModel.checkins_date == date
    )
    # !!!!!!

    result = await session.execute(query)

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Habit with ID={habit_id} for date {date} not found'
        )

    await session.commit()

    return {
        "ok": True,
    }


""" DELETE """
@router.delete("/habits/{habit_id}",
          tags=["Привычки 🚬"],
        summary="Удалить привычку")
async def delete_habit(habit_id: int, session: SessionDep):

    habit = await get_habit_function(session=session, id=habit_id, model=HabitModel)

    await session.delete(habit)
    await session.commit()

    return {
        "ok": True,
    }