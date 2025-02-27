from attrs import define
from typing import List
from enum import Enum

import logging
import rasterio
import numpy as np
from rasterio.crs import CRS
from rasterio.windows import from_bounds
from rio_cogeo.cogeo import cog_validate
from rio_tiler.io import COGReader
from rio_tiler.mosaic import mosaic_reader
from rio_tiler.mosaic.methods import HighestMethod
from rio_tiler.profiles import img_profiles
from rio_tiler.utils import render
from PIL import Image
from io import BytesIO
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.io import MemoryFile


log = logging.getLogger(__name__)

env = {"GDAL_CACHEMAX": 512}

class ImageType(str, Enum):
    """Image Type Enums."""

    png = "png"
    npy = "npy"
    tif = "tif"
    jpg = "jpg"
    webp = "webp"

drivers = dict(jpg="JPEG", png="PNG", tif="GTiff", webp="WEBP")

@define
class WMSBaseServiceHandle:


    def GetMap(geotiff_path, bbox, width: int, height: int, crs, format="image/png", version="1.1.1"):
        log.info(f"CRS {crs}, GeoTiff {geotiff_path}")

        bbox = list(map(float, bbox.split(","))) 

        if len(bbox) != 4:
            raise ValueError(f"Invalid 'BBOX' parameters: {bbox}. Needs 4 coordinates separated by commas")

        if version == "1.3.0":
            if crs == CRS.from_epsg(4326):
                bbox = [
                    bbox[1], bbox[0], bbox[3], bbox[2]
                ]
            elif crs == CRS.from_user_input("CRS:84"):
                crs = CRS.from_epsg(4326)
        # Validate if the GeoTIFF is a valid COG
        try:
            cog_validate(geotiff_path)
        except Exception as e:
            raise ValueError(f"The provided GeoTIFF is not a valid Cloud Optimized GeoTIFF: {e}")

        log.debug(f"RasterIO Open {geotiff_path}")

        # def _reader(src_path):
        #     with rasterio.Env(**env):
        #         with COGReader(src_path) as src_dst:
        #             return src_dst.part(
        #                 bbox=bbox,
        #                 width=width,
        #                 height=height,
        #                 dst_crs=crs,                        
        #                 bounds_crs=crs,
        #             )

        # image, assets_used = mosaic_reader(            
        #     [geotiff_path],
        #     _reader,
        #     pixel_selection=HighestMethod()
        # )

        with COGReader(geotiff_path) as cog:
            image, mask = cog.part(
                bbox=bbox,
                width=width,
                height=height,
                dst_crs=crs                
            )   

        ext = ImageType.png
        driver = drivers[ext.value]
        options = img_profiles.get(driver.lower(), {})

        return render(image, format="png", **options)




        # with rasterio.open(geotiff_path) as src:
        #     log.info(f"GeoTIFF CRS: {src.crs}, Bounds: {src.bounds}" )        

        #     # GeoTIFF CRS
        #     src_crs = src.crs
        #     src_bounds = src.bounds

        #     # log.info(f"BBox {bbox}")
        #     # log.info(f"crs {crs} , src_crs {src_crs}")            
        #     # Reproject bounding box if CRS differs
        #     if crs != str(src_crs):
        #         try: 
        #             transformer = Transformer.from_crs(crs, src_crs, always_xy=True)
        #             log.debug(f"Transformer {transformer}")
        #             minx, miny, maxx, maxy = bbox
        #             minx, miny = transformer.transform(minx, miny)
        #             maxx, maxy = transformer.transform(maxx, maxy)
        #             log.info(f"minx {minx}, miny {miny}")
        #             bbox = (minx, miny, maxx, maxy)                
        #             log.info(f"Reprojected BBox: {bbox}")                
        #         except Exception as e:
        #             log.error(f"Error during reprojection: {e}")
        #             raise

        #     # Clip bbox to source bounds
        #     minx = max(bbox[0], src_bounds.left)
        #     miny = max(bbox[1], src_bounds.bottom)
        #     maxx = min(bbox[2], src_bounds.right)
        #     maxy = min(bbox[3], src_bounds.top)

        #     if (minx, miny, maxx, maxy) != bbox:
        #         log.warning(f"BBox adjusted to fit within source bounds: {(minx, miny, maxx, maxy)}")

        #     # Compute window and validate
        #     try:
        #         window = from_bounds(*bbox, transform=src.transform)        
        #     except Exception as e:
        #         log.error(f"Error computing window: {e}")
        #         raise ValueError("Bounding box is invalid.")
            
        #     # Read data
        #     data = src.read(
        #         window=window, 
        #         out_shape=(src.count, height, width), 
        #         resampling=Resampling.bilinear
        #     )

        #     # Normalize to 8-bit
        #     data_max = data.max()
        #     if data_max == 0:
        #         raise ValueError("Data contains only zeros.")
        #     normalized_data = (data / data_max * 255).astype("uint8")
            
        #     # Write to PNG using Pillow
        #     with MemoryFile() as memfile:
        #         with memfile.open(driver="PNG", width=width, height=height, count=src.count, dtype="uint8") as dst:
        #             dst.write(normalized_data)
        #         png_data = memfile.read()
                    
        #     return png_data
        
    
    