import logging
import rasterio
from rasterio.windows import from_bounds
from rio_cogeo.cogeo import cog_validate
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.io import MemoryFile


log = logging.getLogger(__name__)

class WMSBaseServiceHandle:


    def GetMap(geotiff_path, bbox, width, height, crs, format="image/png"):
        log.info(f"CRS {crs}, GeoTiff {geotiff_path}")

        bbox = tuple(map(float, bbox.split(",")))  # Convert string to tuple of floats        

        # Validate if the GeoTIFF is a valid COG
        try:
            cog_validate(geotiff_path)
        except Exception as e:
            raise ValueError(f"The provided GeoTIFF is not a valid Cloud Optimized GeoTIFF: {e}")

        log.debug(f"RasterIO Open {geotiff_path}")
        with rasterio.open(geotiff_path) as src:
            log.info(f"GeoTIFF CRS: {src.crs}, Bounds: {src.bounds}" )        

            # GeoTIFF CRS
            src_crs = src.crs
            src_bounds = src.bounds

            # log.info(f"BBox {bbox}")
            # log.info(f"crs {crs} , src_crs {src_crs}")            
            # Reproject bounding box if CRS differs
            if crs != str(src_crs):
                try: 
                    transformer = Transformer.from_crs(crs, src_crs, always_xy=True)
                    log.debug(f"Transformer {transformer}")
                    minx, miny, maxx, maxy = bbox
                    minx, miny = transformer.transform(minx, miny)
                    maxx, maxy = transformer.transform(maxx, maxy)
                    log.info(f"minx {minx}, miny {miny}")
                    bbox = (minx, miny, maxx, maxy)                
                    log.info(f"Reprojected BBox: {bbox}")                
                except Exception as e:
                    log.error(f"Error during reprojection: {e}")
                    raise

            # Clip bbox to source bounds
            minx = max(bbox[0], src_bounds.left)
            miny = max(bbox[1], src_bounds.bottom)
            maxx = min(bbox[2], src_bounds.right)
            maxy = min(bbox[3], src_bounds.top)

            if (minx, miny, maxx, maxy) != bbox:
                log.warning(f"BBox adjusted to fit within source bounds: {(minx, miny, maxx, maxy)}")

            # Compute window and validate
            try:
                window = from_bounds(*bbox, transform=src.transform)        
            except Exception as e:
                log.error(f"Error computing window: {e}")
                raise ValueError("Bounding box is invalid.")
            
            # Read data
            data = src.read(
                window=window, 
                out_shape=(src.count, height, width), 
                resampling=Resampling.bilinear
            )

            # Normalize to 8-bit
            data_max = data.max()
            if data_max == 0:
                raise ValueError("Data contains only zeros.")
            normalized_data = (data / data_max * 255).astype("uint8")
            
            # Write to PNG using Pillow
            with MemoryFile() as memfile:
                with memfile.open(driver="PNG", width=width, height=height, count=src.count, dtype="uint8") as dst:
                    dst.write(normalized_data)
                png_data = memfile.read()
                    
            return png_data
        
    
    