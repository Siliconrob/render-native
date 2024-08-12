import time
from itertools import batched
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from icecream import ic

from api.core import reader
from api.models import Country, PagedResult
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


@router.get("/countries", response_model=PagedResult[Country])
async def read_countries(limit: int = 10, page: int = 1) -> Any:
    all_countries = [map_country(country) for country in await reader.get_countries()]
    if limit < 1:
        raise HTTPException(f'Limit must be greater than 0')
    if page < 1:
        raise HTTPException(f'Page must be greater than 0')
    pages = list(batched(all_countries, limit))
    page_index = page - 1
    page_results = [] if len(pages) < page_index else pages[page_index]
    return map_to_page_result(page, page_results, pages, len(all_countries))


def map_to_page_result(page, page_results, pages, total_count):
    response = PagedResult[Country]()
    response.items = len(page_results)
    response.countries = page_results
    response.page = page
    response.page_count = len(pages)
    response.total = total_count
    return response


@router.get("/countries/{code}", response_model=list[Country])
async def read_country_by_id(code: str | None) -> Any:
    response = await reader.get_countries_by_code(code.zfill(3) if code.isnumeric() else code)
    return [map_country(country) for country in response]
