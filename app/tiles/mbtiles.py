from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
import sqlite3
import os
import logging
import morecantile

from rio_tiler.errors import TileOutsideBounds
from rio_tiler.io import Reader
from rio_tiler.profiles import img_profiles

router = APIRouter()

# @router.get("/tiles/WebMercatorQuad/{z}/{x}/{y}")
# def tiles(z: int, x: int, y: int):
#     img = _get_tile(z=z, x=x, y=y, tms="WebMercatorQuad")
#     return Response(content=img, media_type="image/png")

@router.get("/tiles/{layerName}/{z}/{x}/{y}")
def tiles(layerName: str, z: int, x: int, y: int):
    img = _get_tile(z=z, x=x, y=y, tms="WebMercatorQuad", layerName=layerName)
    return Response(content=img, media_type="image/png")

url = "/app/data/lahad_datu_cog.tif"
url = "/app/data/mersing-rgb.tiff"
# url = "https://njogis-imagery.s3.amazonaws.com/2020/cog/I7D16.tif"
def _get_tile(layerName, tms, z, x, y):
    logging.info(f"Request for tile {z}/{x}/{y} for {layerName}")
    if layerName == "lahad_datu":
        url = "/app/data/lahad_datu_cog.tif"
    elif layerName == "mersing":
        url = "/app/data/mersing-rgb.tiff"
    else:
        raise HTTPException(status_code=401)

    try:
        with Reader(url, tms=morecantile.tms.get(tms)) as cog:        
            img = cog.tile(x, y, z, indexes=(1, 2, 3))
    except TileOutsideBounds:
        raise HTTPException(status_code=404)

    prof = img_profiles.get("PNG", {})
    return img.render(img_format="PNG", **prof)


