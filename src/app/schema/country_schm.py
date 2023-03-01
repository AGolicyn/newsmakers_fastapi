import datetime
from fastapi import HTTPException
from pydantic import BaseModel, validator, UUID4, HttpUrl
from typing import Literal


class CountryDate(BaseModel):
    country: Literal['Russia', 'USA', 'Germany']
    date: datetime.date

    @validator('date')
    def date_cant_be_greater_then_today(cls, date):
        if date > datetime.date.today():
            raise HTTPException(status_code=422, detail="Invalid date from future")
        return date


class EntityTitles(BaseModel):
    entities: list[UUID4]


class CountryDateResponse(BaseModel):
    LOC: dict[str, list[UUID4]]
    PER: dict[str, list[UUID4]]
    ORG: dict[str, list[UUID4]]


class EntityTitlesResponse(BaseModel):
    href: HttpUrl
    title: str
