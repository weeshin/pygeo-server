import rasterio
from rasterio.enums import Resampling
from rasterio.transform import Affine
from rasterio.windows import from_bounds
from rio_cogeo.cogeo import cog_validate
from rasterio.io import MemoryFile

class WMSBaseServiceHandle:
    def GetMap(geotiff_path, bbox, width, height, crs, format="image/png"):
        """
        Generate a WMS GetMap response from a GeoTIFF.

        Args:
            geotiff_path (str): Path to the GeoTIFF file.
            bbox (tuple): Bounding box (minx, miny, maxx, maxy) in the requested CRS.
            width (int): Width of the output image.
            height (int): Height of the output image.
            crs (str): Requested CRS (e.g., "EPSG:4326").
            format (str): Output format (e.g., "image/png").

        Returns:
            bytes: The generated image bytes.
        """
        # TODO: Validate CRS
        

        # Validate if the GeoTIFF is a valid COG
        if not cog_validate(geotiff_path):
            raise ValueError("The provided GeoTIFF is not a valid Cloud Optimized GeoTIFF.")

        with rasterio.open(geotiff_path) as src:
            # Convert bounding box to the GeoTIFF CRS
            if not src.transform or src.transform == Affine.identity():
                print("No geotransform found. Using default transform.")
                transform = Affine.translation(0, 0) * Affine.scale(1, -1)  # Identity transform
            else:
                transform = src.transform

            print(transform)
            src_crs = src.crs

            print(src_crs)
            
            # Convert string to tuple of floats
            bbox = tuple(map(float, bbox.split(",")))

            # Reproject bounding box if CRS differs
            if crs != str(src_crs):
                from pyproj import Transformer
                transformer = Transformer.from_crs(crs, src_crs, always_xy=True)
                bbox = transformer.transform_bounds(*bbox)
            
            # Create a window for the requested bounding box
            window = from_bounds(*bbox, transform=src.transform)
            
            # Read the raster data within the window
            data = src.read(window=window, out_shape=(src.count, height, width))
            print(data)

            # Normalize to 8-bit and convert to PNG
            normalized_data = (data / data.max() * 255).astype("uint8")
            print(normalized_data)
            
            if format is "image/jpg":
                driver = "JPG"
            else:
                driver = "PNG"
            
            # Write to PNG using Pillow
            with MemoryFile() as memfile:
                with memfile.open(driver=driver, width=width, height=height, count=src.count, dtype="uint8") as dst:
                    dst.write(normalized_data)
                png_data = memfile.read()
                    
            return png_data