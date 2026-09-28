from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Date

from habittracker.database.db import Base

from datetime import date

# class HabitModel(Base):
#     __tablename__ = "habits"
#
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str] = mapped_column(unique=True)
#     description: Mapped[str | None] = mapped_column(default=None)
#     date_created_habit: Mapped[date] = mapped_column(Date, default=date.today)
#     checking: Mapped[bool] = mapped_column(default=False)


class HabitModel(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(default=None)
    date_created_habit: Mapped[date] = mapped_column(Date, default=date.today)
    checking: Mapped[bool] = mapped_column(default=False)

    checkins: Mapped[list["CheckinHabitModel"]] = relationship(back_populates="habit")


class CheckinHabitModel(Base):
    __tablename__ = "checkins"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_habit: Mapped[int] = mapped_column(ForeignKey('habits.id'), index=True)
    checkins_date: Mapped[date] = mapped_column(Date)

    habit: Mapped["HabitModel"] = relationship(back_populates="checkins")