from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AUTH_")

    database_url: str = "sqlite+aiosqlite:///./auth.db"
    private_key_path: Path = Path("keys/private.pem")

    access_ttl_seconds: int = 10 * 60
    refresh_ttl_seconds: int = 7 * 24 * 60 * 60
    session_max_age_seconds: int = 30 * 24 * 60 * 60
    
    cookie_secure: bool = True


settings = Settings()
