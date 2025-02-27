from rio_tiler.io import Reader

with Reader("D:\\EmDrone\\Lahad Datu\\lahad_datu_cog.tif") as src:
    print(src.dataset)
    print(src.tms.intersect_tms)
    print(src.minzoom)
    print(src.maxzoom)
    print(src.bounds)
    print(src.crs)
    print(src.colormap)


with Reader("D:\\EmDrone\\Lahad Datu\\lahad_datu_cog.tif") as src:
    print("Get Bounds in EPSG:4326")
    print(src.get_geographic_bounds("EPSG:4326"))

