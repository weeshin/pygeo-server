import logging
import numpy as np
from rio_tiler.io import COGReader
from rio_tiler.models import ImageData
from rio_tiler.utils import render
from pyproj import Transformer

log = logging.getLogger(__name__)

class WMSBaseServiceHandle:
    @staticmethod
    def GetMap(geotiff_path, bbox, width, height, crs, format="image/png"):
        log.info(f"CRS {crs}, GeoTiff {geotiff_path}")

        bbox = tuple(map(float, bbox.split(",")))  # Convert string to tuple of floats

        # Open COG and read metadata
        with COGReader(geotiff_path) as cog:
            src_crs = cog.dataset.crs
            src_bounds = cog.dataset.bounds
            log.info(f"GeoTIFF CRS: {src_crs}, Bounds: {src_bounds}")

            # Reproject bounding box if needed
            if crs != str(src_crs):
                try:
                    transformer = Transformer.from_crs(crs, src_crs, always_xy=True)
                    minx, miny, maxx, maxy = bbox
                    minx, miny = transformer.transform(minx, miny)
                    maxx, maxy = transformer.transform(maxx, maxy)
                    bbox = (minx, miny, maxx, maxy)
                    log.info(f"Reprojected BBox: {bbox}")
                except Exception as e:
                    log.error(f"Error during reprojection: {e}")
                    raise

            # Ensure bbox fits within raster bounds
            minx, miny, maxx, maxy = bbox
            if not (-1e7 < minx < 1e7 and -1e7 < maxx < 1e7 and -1e7 < miny < 1e7 and -1e7 < maxy < 1e7):
                raise ValueError(f"Invalid bounding box: {bbox}")

            minx = max(bbox[0], src_bounds[0])
            miny = max(bbox[1], src_bounds[1])
            maxx = min(bbox[2], src_bounds[2])
            maxy = min(bbox[3], src_bounds[3])
            bbox = (minx, miny, maxx, maxy)
            log.info(f"Clipped BBox: {bbox}")

            # Read data using rio_tiler
            img: ImageData = cog.part(
                bbox=(10, 10, 20, 30), dst_crs=crs, max_size=200            
            )

            # Encode the data in PNG (default)
            buff = img.render()

            return buff
