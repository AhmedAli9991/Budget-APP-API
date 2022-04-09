from pydantic import BaseSettings

class Settings(BaseSettings):
    connection_string: str
    access_key: str
    refresh_key: str
    algorithm: str
    access_expire: int
    refresh_expire: int
    class Config:
        env_file = ".env"


settings = Settings()