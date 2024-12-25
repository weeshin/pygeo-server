import rasterio
from rasterio.windows import from_bounds
from rio_cogeo.cogeo import cog_validate
from rasterio.transform import Affine
from rasterio.enums import Resampling
from rasterio.io import MemoryFile
import numpy as np
from PIL import Image

# gdal_translate -of GTiff -co TILED=YES input.tif output_tiled.tif


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
        
        # Write to PNG using Pillow
        with MemoryFile() as memfile:
            with memfile.open(driver="PNG", width=width, height=height, count=src.count, dtype="uint8") as dst:
                dst.write(normalized_data)
            png_data = memfile.read()
                
        return png_data


# Define the GetMap parameters

bbox = "2681963.3968851496,591777.0659296932,2684162.5989161497,593574.0311672932"  # Bounding box in CRS: EPSG:4326
bbox = tuple(map(float, bbox.split(",")))  # Convert string to tuple of floats
srs = "EPSG:32647"
width, height = 768, 627  # Output image dimensions
output_format = "image/png"  # Output format

result = GetMap(geotiff_path="D:\EmDrone\Lahad Datu\lahad_datu_cog.tif", bbox=bbox, width=width, height=height, crs=srs)

# Save result to file
with open("output.png", "wb") as f:
    f.write(result)