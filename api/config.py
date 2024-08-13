import secrets
from typing import Literal

from pydantic import (
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

import time
from cacheout import Cache

cache = Cache(maxsize=8192, ttl=3600, timer=time.time, default=None)  # defaults


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    PROJECT_NAME: str
    BASE_REST_URL: str


settings = Settings()  # type: ignore
