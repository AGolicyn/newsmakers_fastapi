import datetime
from fastapi import HTTPException
from pydantic import BaseModel, validator, UUID4, HttpUrl
from typing import Literal


class CountryDate(BaseModel):
    country: Literal["Russia", "USA", "Germany"]
    date: datetime.date

    @validator("date")
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


class TrendRequest(CountryDate):
    token: str
    day_offset: int

    @validator("day_offset")
    def offset_must_be_positive(cls, day_offset):
        if day_offset <= 0:
            raise HTTPException(status_code=422, detail="Offset should be positive")
        return day_offset

    @validator("token")
    def token_validation(cls, token):
        try:
            tmp_token = token.strip()

            if not tmp_token or len(tmp_token) == 1:
                raise HTTPException(status_code=422, detail="Too short or empty token")
            elif len(tmp_token) in (2, 3):
                token = "%" + tmp_token.lower() + "%"
            else:
                token = "%" + tmp_token.lower()[:-1] + "%"

        except (ValueError, TypeError):
            raise HTTPException(status_code=422, detail=f"'{token}' is not valid token")

        return token


class TrendResponse(BaseModel):
    date: datetime.date
    weight: float
