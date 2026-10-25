from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="GATEWAY_")

    public_key_path: Path = Path("keys/public.pem")

    auth_url: str = "http://127.0.0.1:8002"
    core_url: str = "http://127.0.0.1:8001"

    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
