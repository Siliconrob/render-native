from typing import Optional

from pydantic import BaseModel


class Country(BaseModel):
    code: Optional[str] = None


class Region(BaseModel):
    name: Optional[str] = None


class Language(BaseModel):
    description: Optional[str] = None
