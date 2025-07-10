from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables or a .env file.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        """Builds the full database connection string."""
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # SWAPI configuration
    SWAPI_BASE_URL: str = "https://swapi.info/api"
    # CORS configuration
    CORS_ORIGINS: str = "http://localhost:8000"

    API_BASE_URL: str = "http://localhost:8000"

settings = Settings()