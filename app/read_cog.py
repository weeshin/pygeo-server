import rasterio

# Open the COG file
cog_file_path = "D:\EmDrone\Lahad Datu\lahad_datu_cog.tif"

# with rasterio.open(cog_file_path) as dataset:
#     # Print metadata
#     print("Metadata:", dataset.meta)

#     # Read the data as a NumPy array (e.g., the first band)
#     # band1 = dataset.read(1)

#     # Print shape of the array
#     # print("Band 1 shape:", band1.shape)

#     # Access geospatial transform
#     print("Transform:", dataset.transform)

#     # Access coordinate reference system (CRS)
#     print("CRS:", dataset.crs)

#     # Read band
#     band1 = dataset.read(1)
#     print(band1)


from rio_tiler import reader
from rio_tiler.mosaic import mosaic_reader
from rio_tiler.mosaic.methods import defaults
from rio_tiler.models import ImageData

def tiler(src_path: str, *args, **kwargs) -> ImageData:
    with reader(src_path) as src:
        return src.tile(*args, **kwargs)

x = 2000
y = 2000
z = 10

img, _ = mosaic_reader([cog_file_path], tiler, 
                   x, 
                   y, 
                   z,
                   pixel_selection=defaults.HighestMethod)
print(img)