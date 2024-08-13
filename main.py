import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from icecream import ic
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.middleware.cors import CORSMiddleware

from api.core import reader
from api.main import api_router
from api.config import settings
from api.mapper import map_country

ic.configureOutput(prefix='|> ')


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


limiter = Limiter(key_func=get_remote_address, default_limits=["10000 per day", "1000 per hour", "20 per second"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    duration = time.time()
    results = await reader.get_countries()
    all_countries = [map_country(country) for country in results]
    ic(f'{time.time() - duration}')
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
