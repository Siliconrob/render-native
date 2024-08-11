import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from api.config import settings
from api.models import Region

router = APIRouter()


@router.get("/regions", response_model=Region)
def read_regions() -> Any:
    """
    Get a specific user by id.
    """
    response = Region()
    response.code = None
    return response
