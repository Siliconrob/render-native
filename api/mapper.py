
from itertools import batched
from typing import Any

from icecream import ic

from api.config import cache
from api.models import Country, PagedResult

ic.configureOutput(prefix='|> ')



def map_country(response_country_data: Any) -> Country:
    country_key = ic(
        f'{response_country_data.get('cca2')},{response_country_data.get('ccn3'), {response_country_data.get('cca3')} }')
    cached_country = cache.get(country_key)
    if cached_country is not None:
        ic(f'Use cached value')
        return cached_country
    parsed = Country.model_validate(response_country_data)
    cache.add(country_key, parsed)
    return parsed


def map_to_page_result(page, page_results, page_count, total_count) -> PagedResult[Country]:
    response = PagedResult[Country]()
    response.item_count = len(page_results)
    response.items = page_results
    response.page = page
    response.page_count = page_count
    response.total = total_count
    return response


def get_paged_response(limit: int, page: int, records: list[Any]) -> PagedResult[Any]:
    if limit < 1:
        raise Exception(f'Limit must be greater than 0')
    if page < 1:
        raise Exception(f'Page must be greater than 0')
    pages = list(batched(records, limit))
    page_index = page - 1
    page_results = [] if len(pages) < page else pages[page_index]
    return map_to_page_result(page, page_results, len(pages), len(records))


def paged_dict_response(limit: int, page: int, input_dict: {}) -> dict:
    if limit < 1:
        raise Exception(f'Limit must be greater than 0')
    if page < 1:
        raise Exception(f'Page must be greater than 0')

    start_index = page - 1
    end_index = start_index + limit

    current_index = 0
    paged_values = []
    for (key, value) in input_dict.items():
        if current_index >= end_index:
            break
        if start_index <= current_index < end_index:
            keys = str.split(key, "_")
            key_id = keys.pop()
            key_name = keys.pop()
            paged_values.append({key_name: key_id, "items": value})
        current_index += 1

    q, r = divmod(len(input_dict.keys()), limit)

    return {
        "items": paged_values,
        "item_count": len(paged_values),
        "page": page,
        "page_count": q + 1 if r > 0 else q,
        "total": len(input_dict)
    }