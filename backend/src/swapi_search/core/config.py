from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables or a .env file.
    """
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # SWAPI configuration
    SWAPI_BASE_URL: str = "https://swapi.info/api"

    # Database configuration
    DATABASE_URL: str

    # CORS configuration
    CORS_ORIGINS: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()