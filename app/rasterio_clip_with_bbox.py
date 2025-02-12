import logging
from wms.common import WMSBaseServiceHandle

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the GetMap parameters
bbox = "13170883.7,564058.8,13171139.1,564195.2"
bbox = "13171817.91,563891.44,13172087.027,564049.173"

bbox = "13169182.729196448,562576.5281788978,13171628.714101573,565022.513084024"
bbox = "13171628.714101573,562576.5281788978,13174074.699006699,565022.513084024"
bbox = "13169182.729196448,562576.5281788978,13171628.714101573,565022.513084024"
bbox = "13170099.97353587,563493.7725183209,13170405.72164901,563799.5206314605"
crs = "EPSG:3857"

# bbox = "2681963.3968851496,591777.0659296932,2684162.5989161497,593574.0311672932"  # Bounding box in CRS: EPSG:4326
# bbox = "2683416.1,592616.6,2683697.3,592791.2"
# bbox = "2682429.3,592758.4,2682695.3,592902.5"



# crs = "EPSG:32647"

# bbox = "5.05894384,118.32444962,5.060349,118.326891"
# crs = "EPSG:4326"

width, height = 256, 256  # Output image dimensions
output_format = "image/jpg"  # Output format

logging.info("Start test clip")
result = WMSBaseServiceHandle.GetMap(geotiff_path="D:\EmDrone\Lahad Datu\lahad_datu_cog.tif", bbox=bbox, width=width, height=height, crs=crs)

# Save result to file
with open(f"./tmp/{bbox}_output.png", "wb") as f:
    f.write(result)