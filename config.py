from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    fe_origins: str
    host: str
    fe_url: str
    db_username: str
    db_password: str
    db_name: str
    db_host: str
    db_ssl_mode: str
    client_id: str
    client_secret: str
    redirect_url: str
    project_id: str
    auth_uri: str
    token_uri: str
    auth_provider: str
    google_user_info_url: str
    jwt_secret: str
    jwt_algo: str
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()
