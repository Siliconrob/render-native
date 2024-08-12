import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from api.config import settings
from api.models import Language

router = APIRouter()


@router.get("/languages", response_model=Language)
def read_languages() -> Any:
    """
    Get a specific user by id.
    """
    response = Language()
    response.description = None
    return response
