from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class Translation(BaseModel):
    official: str
    common: str


class Name(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    common: str
    official: str
    native_name: Optional[dict] = None


class Idd(BaseModel):
    root: Optional[str] = None
    suffixes: Optional[list[str]] = None


class Maps(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    google_maps: str
    open_street_maps: str


class Car(BaseModel):
    signs: Optional[list[str]] = None
    side: str


class CoatOfArms(BaseModel):
    pass


class CapitalInfo(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    latlng: Optional[list[float]] = None


class Flags(BaseModel):
    png: str
    svg: str


class Country(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    name: Name
    tld: Optional[list[str]] = None
    cca2: str
    ccn3: Optional[int] = None
    cca3: str
    independent: Optional[bool] = None
    status: str
    un_member: bool
    currencies: Optional[dict] = None
    idd: Idd
    capital: Optional[list[str]] = None
    alt_spellings: list[str]
    region: str
    languages: Optional[dict] = None
    translations: dict[str, Translation]
    latlng: list[float]
    landlocked: bool
    area: float
    demonyms: Optional[dict] = None
    flag: str
    maps: Maps
    population: int
    car: Car
    timezones: list[str]
    continents: list[str]
    flags: Flags
    coat_of_arms: CoatOfArms
    start_of_week: str
    capital_info: CapitalInfo

T = TypeVar('T')

class PagedResult(BaseModel, Generic[T]):
    items: list[T] = []
    item_count: int = 0
    page: int = 1
    page_count: int = 0
    total: int = 0


class Region(BaseModel):
    name: Optional[str] = None
    countries: list[Country] = []


class Language(BaseModel):
    name: Optional[str] = None
    countries: list[Country] = []