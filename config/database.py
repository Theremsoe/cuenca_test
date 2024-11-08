from __future__ import annotations

from typing import Optional
from pydantic import computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class DatabaseConfig(BaseSettings):
    """
    Database configuration
    """

    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="ignore")

    url: Optional[str] = None

    driver: Optional[str] = "postgresql"
    host: Optional[str] = "127.0.0.1"
    port: Optional[int] = 5432
    database: Optional[str] = "forge"
    username: Optional[str] = "forge"
    password: Optional[str] = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def uri(self) -> MultiHostUrl:
        if self.driver == "postgresql":
            return MultiHostUrl.build(
                scheme=self.driver,
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.database,
            )

        return MultiHostUrl.build(scheme="sqlite", host=self.database)

    @staticmethod
    @lru_cache
    def make() -> DatabaseConfig:
        return DatabaseConfig()
