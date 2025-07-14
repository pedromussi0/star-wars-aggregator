# src/swapi_search/core/config.py

import os
import json
import boto3
from typing import Optional
from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables.
    This version is "cloud-aware" and can fetch DB credentials
    from AWS Secrets Manager when running in a deployed environment.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='ignore')

    # --- Standard App Settings ---
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SWAPI_BASE_URL: str = "https://swapi.info/api"
    CORS_ORIGINS: str = "http://localhost:8000"
    API_BASE_URL: str = "http://localhost:8000"

    # --- AWS & Database Credentials ---
    # OPTIONAL. loaded from .env for local dev.
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    DATABASE_SECRET_ARN: Optional[str] = None

    def __init__(self, **values):
        """
        Custom initializer to fetch secrets from AWS Secrets Manager if the ARN is present.
        """
        super().__init__(**values)
        if self.DATABASE_SECRET_ARN:
            print("DATABASE_SECRET_ARN detected. Fetching secrets from AWS Secrets Manager.")
            try:
                session = boto3.session.Session()
                client = session.client(service_name='secretsmanager')
                get_secret_value_response = client.get_secret_value(SecretId=self.DATABASE_SECRET_ARN)
                secret = json.loads(get_secret_value_response['SecretString'])
                
                self.POSTGRES_USER = secret.get('username')
                self.POSTGRES_PASSWORD = secret.get('password')
                self.POSTGRES_HOST = secret.get('host')
                self.POSTGRES_PORT = secret.get('port')
                self.POSTGRES_DB = secret.get('dbname')
                print("Successfully loaded secrets into configuration.")
            except Exception as e:
                print(f"FATAL: Could not fetch or parse secrets from AWS Secrets Manager: {e}")
                raise e

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        """Dynamically builds the database connection string."""
        if not all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_DB]):
            
            return "postgresql+psycopg2://user:pass@host/db" 
            
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @computed_field
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Dynamically builds the async database connection string."""
        if not all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_DB]):
            return "postgresql+asyncpg://user:pass@host/db" 

        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
