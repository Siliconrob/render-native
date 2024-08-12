import time
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from icecream import ic

from api.core import reader
from api.models import Country
from cacheout import Cache

router = APIRouter()

ic.configureOutput(prefix='|> ')
cache = Cache(maxsize=256, ttl=60, timer=time.time, default=None)  # defaults


def map_country(response_country_data: Any) -> Country:
    country_key = ic(f'{response_country_data.get('cca2')},{response_country_data.get('ccn3'), {response_country_data.get('cca3')}}')
    cached_country = cache.get(country_key)
    if cached_country is not None:
        ic(f'Use cached value')
        return cached_country
    parsed = ic(Country.model_validate(response_country_data))
    cache.add(country_key, parsed)
    return parsed


@router.get("/countries", response_model=list[Country])
async def read_countries(limit: int = 10, page: int = 1) -> Any:
    response = await reader.get_countries()
    return [map_country(country) for country in response]


@router.get("/countries/{code}", response_model=list[Country])
async def read_country_by_id(code: str | None) -> Any:
    response = await reader.get_countries_by_code(code.zfill(3) if code.isnumeric() else code)
    return [map_country(country) for country in response]
