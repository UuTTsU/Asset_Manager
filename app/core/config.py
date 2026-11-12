from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'App Name'
    debug: bool = True

    #db validation
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_url: str
    postgres_port: int
    postgres_host: str

    #mongodb validation
    mongo_db: str
    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int



    #minIO validation
    minio_root_user: str
    minio_root_password: str

    #Redis
    redis_password: str

    model_config= SettingsConfigDict(env_file='.env')

