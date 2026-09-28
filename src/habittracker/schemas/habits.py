import re

from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date


class HabitAddSchema(BaseModel):

    name: str = Field(default='Название привычки', min_length=1, max_length=50)
    description: str | None = Field(default='Описание (необязательное поле)', max_length=150)

    model_config = ConfigDict(from_attributes=True)


    @field_validator('name')
    @classmethod
    def name_validator(cls, value: str) -> str:

        symbols = r'[!@#$%^&*=+;~-]'

        if re.search(symbols, value):
            raise ValueError(f'Недопустимое имя привычки {cls}')

        if not value.strip():
            raise ValueError('Название привычки не может состоять из одних пробелов')

        return value.strip()



class HabitSchema(HabitAddSchema):
    id: int = Field(frozen=True)
    date_created_habit: date = Field(frozen=True)
    checking: bool = Field(default=False)

    # model_config = ConfigDict(from_attributes=True, extra='forbid')
    model_config = ConfigDict(from_attributes=True)




class CheckinHabitSchema(BaseModel):
    id: int
    id_habit: int
    checkins_date: date = Field(frozen=True)

    model_config = ConfigDict(from_attributes=True)
