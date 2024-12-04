from fastapi import APIRouter, Query, HTTPException
from starlette.responses import Response
from .renderer import render_map

router = APIRouter()

@router.get("/wms", summary="Web Map Service")
async def wms(
    service: str = Query(..., description="Service type (WMS)"),
    request: str = Query(..., description="Request type (GetMap)"),
    layers: str = Query(..., description="Comma-separated layer names"),
    bbox: str = Query(..., description="Bounding box (minx,miny,maxx,maxy)"),
    width: int = Query(..., description="Map width in pixels"),
    height: int = Query(..., description="Map height in pixels"),
    crs: str = Query("EPSG:4326", description="Coordinate Reference System"),
    format: str = Query("image/png", description="Output format"),
):
    # Validate the service and request types
    if service.upper() != "WMS" or request.upper() != "GETMAP":
        raise HTTPException(status_code=400, detail="Invalid service or request type")
    
    # Parse the bounding box
    try:
        minx, miny, maxx, maxy = map(float, bbox.split(","))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid bounding box format")
    
    # Render the map
    image = render_map(layers, (minx, miny, maxx, maxy), width, height, crs)
    
    # Return the map image
    if format.lower() == "image/png":
        return Response(image, media_type="image/png")
    else:
        raise HTTPException(status_code=400, detail="Unsupported format")
