import logging

from app import __version__ as app_version
from fastapi import FastAPI
from app.wms.router import router as wms_router
from app.wmts.router import router as wmts_router
from app.tiles.mbtiles import router as mbtiles_router
from app.config import Settings

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
)
logger = logging.getLogger(__name__)  # Create a logger for this module
logging.getLogger("rio-tiler").setLevel(logging.ERROR)
logging.getLogger("rasterio").setLevel(logging.ERROR)

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    This is a WMS server built with FastAPI. It supports the following operations:
    """,
    version=app_version,
)

app.include_router(wms_router, prefix="/api")
app.include_router(wmts_router)
app.include_router(mbtiles_router, prefix="/api")

# Test root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI WMS Server"}
