import uuid
from collections.abc import Iterable
from functools import partial
from operator import is_not
from typing import Any, Dict
from api.models import Country


def search_all_countries(find: str, items_to_search: list[Country]) -> list[Country]:
    if find is None or find.strip() == "":
        return items_to_search
    matches = []
    for country in items_to_search:
        if search_country(find.strip(), country):
            matches.append(country)
        continue
    return list(filter(partial(is_not, None), matches))


def search_country(search_term: str, input_country: Country) -> bool:
    if search_term is None or search_term.strip() == "":
        return False
    item = flatten_object(input_country)
    search_values = map(str, list(item.values()))
    exists = lambda x: search_term in x
    matched = len(list(filter(exists, search_values))) > 0
    return matched


# https://skeptric.com/flatten-object-python/index.html
def flatten_object(nested: Any, sep: str = "_", prefix="") -> Dict[str, Any]:
    """Flattens nested dictionaries and iterables

    The key to a leaf (something is not list-like or a dictionary)
    is the accessors to that leaf from the root separated by sep
    prefixed with prefix.

    If flattening results in a duplicate key raises a ValueError.

    For example:
      flatten_object([{'a': {'b': 'c'}}, [1]],
                     prefix='nest_') == {'nest_0_a_b': 'c', 'nest_1_0': 1}
    """
    ans = {}

    def flatten(x, name=()):
        if isinstance(x, dict):
            for k, v in x.items():
                flatten(v, name + (str(k),))
        elif isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for i, v in enumerate(x):
                flatten(v, name + (str(i),))
        else:
            key = sep.join(name)
            if key in ans:
                name = f'{name}{sep}{uuid.uuid4().hex}'
                # raise ValueError(f"Duplicate key {key}")
            ans[prefix + sep.join(name)] = x

    flatten(nested)
    return ans
