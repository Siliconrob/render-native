from typing import Any

from fastapi import APIRouter, HTTPException

from api.core import reader
from api.mapper import cache, paged_dict_response
from api.models import Region
from api.routes.countries import map_country

router = APIRouter()


@router.get("/regions", response_model=dict)
async def read_regions(limit: int = 10, page: int = 1) -> Any:
    all_regions = await mapped_regions()
    return paged_dict_response(limit, page, all_regions)


@router.get("/regions/{id}", response_model=list)
async def read_region_by_id(id: str) -> Any:
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
