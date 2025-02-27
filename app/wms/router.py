from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import Response
from typing import Optional, List
from attr import field
import logging as log
from .wms111 import generate_xml_response as generate_xml_response_111, GetMap as GetMap_111
from .wms130 import GetCapabilities as GetCapabilities_130, GetMap as GetMap_130
from .renderer import render_map
from .data_loader import Service
from app import database
from sqlalchemy.orm import Session
from rio_tiler.io import Reader
from rio_tiler.profiles import img_profiles
from rasterio.warp import transform_bounds
import numpy as np
import io


router = APIRouter()

supported_version: List[str] = field(default=["1.0.0", "1.1.1", "1.3.0"])

@router.get("/wms", 
            response_class=Response, 
            responses={
                200: {
                    "description": "Web Map Service responses",
                }
            },
            summary="Web Map Service")
async def wms(
    service: str = Query(..., description="Service type (WMS)"),
    request: str = Query(..., description="Request type (GetMap)"),
    version: str = Query(..., description="Version. Value is 1.0.0, 1.1.0, 1.1.1, 1.3.0"),
    layers: Optional[str] = Query(None, description="Comma-separated layer names"),
    bbox: str = Query(None, description="Bounding box (minx,miny,maxx,maxy)"),
    width: int = Query(None, description="Map width in pixels"),
    height: int = Query(None, description="Map height in pixels"),
    crs: str = Query("EPSG:4326", description="Coordinate Reference System"),
    srs: str = Query("EPSG:3857", description="Spatial Reference System (e.g., EPSG:4326, EPSG:3857)"),
    format: str = Query("image/png", description="Output format"),
    db: Session = Depends(database.get_db)
):
    log.debug(f"Version {version}, bbox {bbox}, csr {crs}")
    match version:
        case "1.1.0":
            log.debug("1.1.0")            
        case "1.1.1":
            log.debug("1.1.1")
        case "1.3.0":
            log.debug("1.3.0")
        case _:
            log.debug ("default")

    # Processing request to Support 'GetCapabilities', 'GetMap' and 'GetFeatureInfo    
    if request.lower() == "getcapabilities":
        serviceModel = Service(name= 'WMS', title="Example WMS Service 1", abstract="This is an example WMS API.")
        xml_content = GetCapabilities_130(serviceModel=serviceModel, db=db)        
        return Response(content=xml_content, media_type="application/xml")
    
    
    if request.lower() == "getmap":     
        if width < 10 or height < 10:
            raise HTTPException(status_code=404, detail="Map heigh or width invalid.")            

    # if version not in supported_version:
    #     raise HTTPException(status_code=404, detail="Unsupported version. Allowed versions include: {self.supported_version}")

    # match version:
    #     case "1.1.0":
    #         log.debug("1.1.0")            
    #     case "1.1.1":
    #         content = GetMap_111(geotiff_path="./data/lahad_datu_cog.tif", bbox=bbox, width=width, height=height, crs=crs)
    #     case "1.3.0":
    #         content = GetMap_130(geotiff_path="./data/lahad_datu_cog.tif", bbox=bbox, width=width, height=height, crs=crs)
    #         log.debug(f"content {content}");
    #     case _:
    #         print ("default")    

        
    # Default SRS (assumes input GeoTIFF is in EPSG:4326)
    DEFAULT_SRS = "EPSG:4326"
    bands = "1,2,3"  # Default bands
    bands = list(map(int, bands.split(",")))  # Convert bands to list of integers
    minx, miny, maxx, maxy = map(float, bbox.split(","))  # Convert bbox to floats

    # Reproject bounding box if needed
    if srs != DEFAULT_SRS:
        minx, miny, maxx, maxy = transform_bounds(srs, DEFAULT_SRS, minx, miny, maxx, maxy)

    with Reader("/app/data/lahad_datu_cog.tif") as src:
        # Read data from the bounding box
        img = src.part((minx, miny, maxx, maxy), width=width, height=height)        
        print(img.data.dtype)
        print(f"format {format}")

        if format.lower() == "image/png":
            imageFormat = "PNG"                    
        else:
            imageFormat = "JPEG"
        
        # Render the image correctly using rio-tiler's `render()`
        img_bytes = img.render(
            img_format=imageFormat.upper(),  # Ensure format is in uppercase (PNG, JPEG)
            **img_profiles.get(imageFormat.lower(), {})  # Use the appropriate image profile
        )

        return Response(content=img_bytes, media_type=format)

    # return Response(
    #     content=content,
    #     media_type=format
    # )
        
    
    return Response(content="<error>Unsupported request type</error>", media_type="application/xml")

