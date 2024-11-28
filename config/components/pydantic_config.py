# config/components/pydantic_config.py
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / "config" / ".env"

class AppConfig(BaseSettings):
    secret_key: str
    debug: bool = False
    language_code: str = "ru-RU"
    time_zone: str = "UTC"
    static_url: str = "static/"
    allowed_hosts: List[str] = ["127.0.0.1"]

    class Config:
        extra = "allow"
        env_file = ENV_PATH

class PrimaryDatabaseConfig(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str = "127.0.0.1"
    db_port: int = 5432
    search_path: str = "public,content"

    class Config:
        extra = "allow"
        env_prefix = "PRIMARY_"
        env_file = ENV_PATH

class SecondaryDatabaseConfig(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str = "127.0.0.1"
    db_port: int = 5432

    class Config:
        extra = "allow"
        env_prefix = "SECONDARY_"
        env_file = ENV_PATH


app_config = AppConfig()
primary_db_config = PrimaryDatabaseConfig()
secondary_db_config = SecondaryDatabaseConfig()