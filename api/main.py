from fastapi import APIRouter

from api.routes import countries, languages, regions

api_router = APIRouter()
api_router.include_router(countries.router, tags=["Countries"])
api_router.include_router(languages.router, tags=["Languages"])
api_router.include_router(regions.router, tags=["Regions"])
