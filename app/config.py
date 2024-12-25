from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    PROJECT_NAME: str = "pygeo-server"
    ENV: str = "development"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    class Config:
        env_file = ".env"


settings = Settings()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
)
logger = logging.getLogger(__name__)  # Create a logger for this module