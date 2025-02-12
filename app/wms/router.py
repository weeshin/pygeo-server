from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import Response
from typing import Optional
import logging as log
from .wms111 import generate_xml_response as generate_xml_response_111, GetMap as GetMap_111
from .wms130 import GetCapabilities as GetCapabilities_130, GetMap as GetMap_130
from .renderer import render_map
from .data_loader import Service
from app import database
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/wms", response_class=Response, summary="Web Map Service")
async def wms(
    service: str = Query(..., description="Service type (WMS)"),
    request: str = Query(..., description="Request type (GetMap)"),
    version: str = Query(..., description="Version. Value is 1.0.0, 1.1.0, 1.1.1, 1.3.0"),
    layers: Optional[str] = Query(None, description="Comma-separated layer names"),
    bbox: str = Query(None, description="Bounding box (minx,miny,maxx,maxy)"),
    width: int = Query(None, description="Map width in pixels"),
    height: int = Query(None, description="Map height in pixels"),
    crs: str = Query("EPSG:4326", description="Coordinate Reference System"),
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

        match version:
            case "1.1.0":
                log.debug("1.1.0")            
            case "1.1.1":
                content = GetMap_111(geotiff_path="./data/lahad_datu_cog.tif", bbox=bbox, width=width, height=height, crs=crs)
            case "1.3.0":
                content = GetMap_130(geotiff_path="./data/lahad_datu_cog.tif", bbox=bbox, width=width, height=height, crs=crs)
                # log.debug(f"content {content}");
            case _:
                print ("default")    

        return Response(
            content=content,
            media_type=format
        )
        
    
    return Response(content="<error>Unsupported request type</error>", media_type="application/xml")

