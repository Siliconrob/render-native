import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from icecream import ic

from api.config import settings
from api.core import reader
from api.models import Country

router = APIRouter()

ic.configureOutput(prefix='|> ')


@router.get("/countries", response_model=list[Country])
async def read_countries() -> Any:
    response = await reader.get_countries()
    return [Country(code=country.get('cca2')) for country in response]


@router.get("/countries/{code}", response_model=list[Country])
async def read_country_by_id(code: str | None) -> Any:
    response = await reader.get_countries()
    return [Country(code=country.get('cca2')) for country in response]
