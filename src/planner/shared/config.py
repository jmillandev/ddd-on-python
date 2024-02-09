from typing import Optional

from pydantic import MongoDsn, PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[str] = None
    ENVIROMENT: str = "production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SECRET_KEY: str

    MONGO_SERVER: str
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DETAILS: Optional[str] = None
    MONGO_DB: str

    @field_validator("DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data.get("POSTGRES_USER"),
            password=info.data.get("POSTGRES_PASSWORD"),
            host=info.data.get("POSTGRES_SERVER"),
            path=f"{info.data.get('POSTGRES_DB') or ''}",
        ).unicode_string()

    @field_validator("MONGO_DETAILS", mode="before")
    @classmethod
    def assemble_mongo_connection(cls, v: Optional[str], info: ValidationInfo) -> str:
        return MongoDsn.build(
            scheme="mongodb",
            host=info.data.get("MONGO_SERVER"),
            username=info.data.get("MONGO_USER"),
            password=info.data.get("MONGO_PASSWORD"),
            query="uuidRepresentation=standard",
        ).unicode_string()


settings = Settings()  # type: ignore[call-arg]
