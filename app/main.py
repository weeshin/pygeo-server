from fastapi import FastAPI
from wms.router import router as wms_router

app = FastAPI(title="FastAPI WMS Server")

app.include_router(wms_router, prefix="/api")

# Test root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI WMS Server"}
