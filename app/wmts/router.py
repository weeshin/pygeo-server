from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import Response

router = APIRouter()

@router.get("/wmts", 
            response_class=Response, 
            summary="Web Map Service")
async def wmts(
    service: str = Query(..., description="Service type (WMTS)"),
    request: str = Query(..., description="Request type (GetTile)"),
    version: str = Query(..., description="Version. Value is 1.0.0, 1.1.0, 1.1.1, 1.3.0"),
    layer: str = Query(..., description="Layer name"),
    style: str = Query(..., description="Style name"),
    tilematrixset: str = Query(..., description="Tile matrix set"),
    tilematrix: str = Query(..., description="Tile matrix"),
    tilerow: int = Query(..., description="Tile row"),
    tilecol: int = Query(..., description="Tile column"),
    format: str = Query("image/png", description="Output format"),
):
    return Response(content="WMTS", media_type="text/plain")


