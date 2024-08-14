from operator import attrgetter
from typing import Any

from fastapi import APIRouter, HTTPException
from icecream import ic

from api.core import reader
from api.core.finder import search_all_countries
from api.mapper import cache, paged_dict_response, sort_key
from api.models import Region
from api.routes.countries import map_country

ic.configureOutput(prefix='|> ')
router = APIRouter()


@router.get("/regions", response_model=dict)
async def read_regions(limit: int = 10, page: int = 1, find: str = None, sort_by: str = None, sort_desc: bool = True) -> Any:
    all_regions = await mapped_regions()
    if find is None or find.strip() == '':
        try:
            [v.sort(key=attrgetter(sort_key(sort_by)), reverse=not sort_desc) for (k, v) in all_regions.items()]
        except AttributeError as error:
            ic(error)
        return paged_dict_response(limit, page, all_regions)
    filtered = {}
    for (k, v) in all_regions.items():
        region_matches = search_all_countries(find, v)
        if region_matches is None or len(region_matches) == 0:
            continue
        try:
            region_matches.sort(key=attrgetter(sort_key(sort_by)), reverse=not sort_desc)
        except AttributeError as error:
            ic(error)
        filtered[k] = region_matches
    return paged_dict_response(limit, page, filtered)


@router.get("/regions/{id}", response_model=list)
async def read_region_by_id(id: str, sort_by: str = None, sort_desc: bool = True) -> Any:
    region_key = cache_key(id)
    region = cache.get(region_key)
    if region is None:
        regions = await mapped_regions()
        region = regions.get(region_key)
        if region is None:
            raise HTTPException(status_code=404, detail="Region not found")
        cache.set(region_key, region)
    result = Region()
    result.name = id.lower()
    try:
        region.sort(key=attrgetter(sort_key(sort_by)), reverse=not sort_desc)
    except AttributeError as error:
        ic(error)
    result.countries = region
    return [result]


def cache_key(id: str = "all") -> str:
    return f'regions_{id.lower()}'


async def mapped_regions() -> dict:
    all_key = cache_key()
    regions = cache.get(all_key)
    if regions is None:
        all_countries = [map_country(country) for country in await reader.get_countries()]
        regions = get_regions(all_countries)
        cache.set(all_key, regions)
    return regions


def get_regions(all_countries):
    regions = {}
    for country in all_countries:
        key = cache_key(country.region)
        current_region = regions.get(key)
        if current_region is None:
            regions[key] = [country]
            continue
        current_region.append(country)
        regions[key] = current_region
    return regions
