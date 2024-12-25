import rasterio

# Open the COG file
cog_file_path = "D:\\Merbau Pulas\\merbau_pulas_compressed.tif"

with rasterio.open(cog_file_path) as dataset:
    # Print metadata
    print("Metadata:", dataset.meta)

    # Read the data as a NumPy array (e.g., the first band)
    # band1 = dataset.read(1)

    # Print shape of the array
    # print("Band 1 shape:", band1.shape)

    # Access geospatial transform
    print("Transform:", dataset.transform)

    # Access coordinate reference system (CRS)
    print("CRS:", dataset.crs)
