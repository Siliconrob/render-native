from dbm import error
from operator import attrgetter
from typing import Any

from fastapi import APIRouter, HTTPException
from icecream import ic

from api.core import reader
from api.core.finder import search_all_countries
from api.mapper import cache, paged_dict_response, sort_key
from api.models import Language
from api.routes.countries import map_country

ic.configureOutput(prefix='|> ')
router = APIRouter()


@router.get("/languages", response_model=dict)
async def read_languages(limit: int = 10, page: int = 1, find: str = None, sort_by: str = None, sort_desc: bool = True) -> Any:
    all_languages = await mapped_languages()
    if find is None or find.strip() == '':
        try:
            [v.sort(key=attrgetter(sort_key(sort_by)), reverse=not sort_desc) for (k, v) in all_languages.items()]
        except AttributeError as error:
            ic(error)
        return paged_dict_response(limit, page, all_languages)
    filtered = {}
    for (k, v) in all_languages.items():
        language_matches = search_all_countries(find, v)
        if language_matches is None or len(language_matches) == 0:
            continue
        try:
            language_matches.sort(key=attrgetter(sort_key(sort_by)), reverse=not sort_desc)
        except AttributeError as error:
            ic(error)
        filtered[k] = language_matches
    return paged_dict_response(limit, page, filtered)


@router.get("/languages/{id}", response_model=list[Language])
async def read_language_by_id(id: str, sort_by: str = None, sort_desc: bool = True) -> Any:
    language_key = cache_key(id)
    language = cache.get(language_key)
    if language is None:
        languages = await mapped_languages()
        language = languages.get(language_key)
        if language is None:
            raise HTTPException(status_code=404, detail="Language not found")
        cache.set(language_key, language)
    result = Language()
    result.name = id.lower()
    found_languages = language.values()
    try:
        found_languages.sort(key=attrgetter(sort_key(sort_by)), reverse=not sort_desc)
    except AttributeError as error:
        ic(error)
    result.countries = found_languages
    return [result]


def cache_key(id: str = "all") -> str:
    return f'languages_{id.lower()}'


async def mapped_languages() -> dict:
    all_key = cache_key()
    languages = cache.get(all_key)
    if languages is None:
        all_countries = [map_country(country) for country in await reader.get_countries()]
        languages = get_languages(all_countries)
        cache.set(all_key, languages)
    return languages


def get_languages(all_countries):
    languages = {}
    for country in all_countries:
        if country.languages is None:
            continue
        for (abbr, full) in country.languages.items():
            languages = add_language(cache_key(abbr), country, languages)
            languages = add_language(cache_key(full), country, languages)
    return languages


def add_language(abbr_key: str, country, languages: dict) -> dict:
    current_language_abbr = languages.get(abbr_key)
    if current_language_abbr is None:
        languages[abbr_key] = [country]
    else:
        current_language_abbr.append(country)
        languages[abbr_key] = current_language_abbr
    return languages
