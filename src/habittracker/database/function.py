from datetime import datetime

from sqlalchemy import update
from sqlalchemy.ext.asyncio import async_sessionmaker

from habittracker.models.habits import HabitModel


async def update_database(session_factory: async_sessionmaker):
    async with session_factory() as session:
        try:
            query = update(HabitModel).where(HabitModel.checking == True).values(checking=False)
            await session.execute(query)
            await session.commit()
            print(f" БД успешно обновлена асинхронно в {datetime.now()}")
            return
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при обновлении БД: {e}")
            return