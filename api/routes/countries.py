import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from icecream import ic

from api.config import settings
from api.core import reader
from api.models import Country

router = APIRouter()

ic.configureOutput(prefix='|> ')


def map_country(response_country_data: Any) -> Country:
    parsed = Country.model_validate(ic(response_country_data))
    return parsed


@router.get("/countries", response_model=list[Country])
async def read_countries(limit: int = 10, page: int = 1) -> Any:
    response = await reader.get_countries()
    return [map_country(country) for country in response]


@router.get("/countries/{code}", response_model=list[Country])
async def read_country_by_id(code: str | None) -> Any:
    response = await reader.get_countries_by_code(code.zfill(3) if code.isnumeric() else code)
    return [map_country(country) for country in response]
