from rio_tiler.constants import WEB_MERCATOR_CRS
from rio_tiler.io import Reader
from rio_tiler.models import ImageData

with Reader("D:\\EmDrone\\Lahad Datu\\lahad_datu_cog.tif") as src:
    # src.tile(tile_x, tile_y, tile_z, **kwargs)
    img = src.tile(1, 1, 14, tilesize=256)
    assert isinstance(img, ImageData)
    assert img.crs == WEB_MERCATOR_CRS
    assert img.assets == ["D:\\EmDrone\\Lahad Datu\\lahad_datu_cog.tif"]

# With indexes
# with Reader("D:\\EmDrone\\Lahad Datu\\lahad_datu_cog.tif") as src:
#     img = src.tile(1, 2, 3, tilesize=256, indexes=1)
#     assert img.count == 1

# With expression
# with Reader("D:\\EmDrone\\Lahad Datu\\lahad_datu_cog.tif") as src:
#     img = src.tile(1, 2, 3, tilesize=256, expression="B1/B2")
#     assert img.count == 1