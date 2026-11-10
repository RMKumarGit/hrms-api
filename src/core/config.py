from functools import lru_cache
import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='HRMS_API_',
        extra='ignore'
    )

    database_url: str = os.getenv('HRMS_API_DATABASE_URL')
    sql_echo:bool = os.getenv('HRMS_API_SQL_ECHO')
    cors_origins: list[str] = []
    secret_key:str = os.getenv('HRMS_API_JWT_SECRET_KEY')
    algorithm:str = 'HS256'
    access_token_expire_mins:int = 15

@lru_cache
def get_settings() -> Settings:
    return Settings()