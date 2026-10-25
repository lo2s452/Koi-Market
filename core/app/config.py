from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"

    PUBLIC_KEY_PATH: Path = Path("keys/public.pem")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
