from typing import Optional

from pydantic import BaseModel, Field


class Country(BaseModel):
    code: str = Field()

class Region(BaseModel):
    name: Optional[str] = None


class Language(BaseModel):
    description: Optional[str] = None
