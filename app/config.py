from pydantic import field_validator
from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    PROJECT_NAME: str = "pygeo-server"
    cors_origins: str = "*"
    cors_allow_methods: str = "GET"
    ENV: str = "development"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    @field_validator("cors_origins")
    def parse_cors_origins(cls, value):
        return [origin.strip() for origin in value.split(",")]
    
    @field_validator("cors_allow_methods")
    def parse_cors_allow_methods(cls, value):
        return [method.strip().upper() for method in value.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
)
logger = logging.getLogger(__name__)  # Create a logger for this module