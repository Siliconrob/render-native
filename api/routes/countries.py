from typing import Any
from fastapi import APIRouter, HTTPException
from icecream import ic

from api.core import reader
from api.core.finder import search_all_countries
from api.mapper import map_country, get_paged_response, sort_key
from api.models import Country, PagedResult
from operator import attrgetter

ic.configureOutput(prefix='|> ')
router = APIRouter()


@router.get("/countries", response_model=PagedResult[Country])
async def read_countries(limit: int = 10, page: int = 1, find: str = None, sort_by: str = None, sort_desc: bool = True) -> Any:
    all_countries = search_all_countries(find, [map_country(country) for country in await reader.get_countries()])
    try:
        all_countries.sort(key=attrgetter(sort_key(sort_by)), reverse=not sort_desc)
    except AttributeError as error:
        ic(error)
    return get_paged_response(limit, page, all_countries)


@router.get("/countries/{code}", response_model=PagedResult[Country])
async def read_country_by_id(code: str | None, limit: int = 10, page: int = 1, sort_by: str = None, sort_desc: bool = True) -> Any:
    api_response = await reader.get_countries_by_code(code.zfill(3) if code.isnumeric() else code)
    countries_match = [map_country(country) for country in api_response]
    try:
        countries_match.sort(key=attrgetter(sort_key(sort_by)), reverse=not sort_desc)
    except AttributeError as error:
        ic(error)
    return get_paged_response(limit, page, countries_match)
