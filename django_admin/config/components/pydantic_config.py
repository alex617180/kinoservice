# config/components/pydantic_config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from typing import List
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / "config" / ".env"

class BaseConfig(BaseSettings):
    """
    Базовый класс для конфигураций, обеспечивает общие настройки.
    """
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
    )


class AppConfig(BaseConfig):
    """
    Класс конфигурации приложения.
    """
    secret_key: SecretStr = Field(validation_alias="SECRET_KEY")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    language_code: str = Field(default="ru-RU", validation_alias="LANGUAGE_CODE")
    time_zone: str = Field(default="UTC", validation_alias="TIME_ZONE")
    allowed_hosts: List[str] = Field(default=["127.0.0.1"], validation_alias="ALLOWED_HOSTS")

class PrimaryDatabaseConfig(BaseConfig):
    """
    Класс конфигурации основной базы данных.
    """
    db_name: str = Field(validation_alias="PRIMARY_DB_NAME")
    db_user: str = Field(validation_alias="PRIMARY_DB_USER")
    db_password: SecretStr | None = Field(default=None, validation_alias="PRIMARY_DB_PASSWORD")
    db_host: str = Field(default="127.0.0.1", validation_alias="PRIMARY_DB_HOST")
    db_port: int = Field(default=5432, validation_alias="PRIMARY_DB_PORT")
    search_path: str = Field(default="public,content", validation_alias="PRIMARY_DB_SEARCH_PATH")

class SecondaryDatabaseConfig(BaseConfig):
    """
    Класс конфигурации вторичной базы данных.
    """
    db_name: str = Field(validation_alias="SECONDARY_DB_NAME")
    db_user: str = Field(validation_alias="SECONDARY_DB_USER")
    db_password: SecretStr | None = Field(default=None, validation_alias="SECONDARY_DB_PASSWORD")
    db_host: str = Field(default="127.0.0.1", validation_alias="SECONDARY_DB_HOST")
    db_port: int = Field(default=5432, validation_alias="SECONDARY_DB_PORT")

app_config = AppConfig()
primary_db_config = PrimaryDatabaseConfig()
secondary_db_config = SecondaryDatabaseConfig()
