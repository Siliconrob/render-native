import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from api.config import settings
from api.models import Country

router = APIRouter()


@router.get("/countries", response_model=Country)
def read_countries() -> Any:
    """
    Get a specific user by id.
    """
    response = Country()
    response.code = None
    return response


@router.get("/countries/{code}", response_model=Country)
def read_country_by_id(code: str | None) -> Any:
    """
    Get a specific user by id.
    """
    response = Country()
    response.code = code
    return response
