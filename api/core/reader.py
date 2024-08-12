from typing import Any

import httpx
from async_lru import alru_cache
from icecream import ic

from api.core import agents

ic.configureOutput(prefix='|> ')

from api.config import settings


@alru_cache(ttl=3600)
async def get_countries_by_code(code) -> Any:
    if settings.BASE_REST_URL is None or settings.BASE_REST_URL == "":
        raise Exception(f'BASE_REST_URL must be set')

    headers = ic({"User-Agent": agents.random_agent()})
    async with httpx.AsyncClient() as client:
        r = await client.get(ic(f'{settings.BASE_REST_URL}/alpha/{code}'), headers=headers)
        return r.raise_for_status().json()
    return None


@alru_cache(ttl=3600)
async def get_countries() -> Any:
    if settings.BASE_REST_URL is None or settings.BASE_REST_URL == "":
        raise Exception(f'BASE_REST_URL must be set')

    headers = ic({"User-Agent": agents.random_agent()})
    async with httpx.AsyncClient() as client:
        r = await client.get(ic(f'{settings.BASE_REST_URL}/all'), headers=headers)
        return r.raise_for_status().json()
    return None
