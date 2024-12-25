import xml.etree.ElementTree as ET
import io
import rasterio
import json
import logging as log
from rasterio.enums import Resampling
from rasterio.transform import Affine
from rasterio.windows import from_bounds
from rio_cogeo.cogeo import cog_validate
from rasterio.io import MemoryFile
from fastapi.responses import StreamingResponse
import numpy as np
from io import BytesIO
from PIL import Image
import socket
from .data_loader import Service
from app.crud import *
from app.models import *
from sqlalchemy.orm import Session
from .common import WMSBaseServiceHandle


# Define the namespaces and attributes
namespaces = {
    "xmlns": "http://www.opengis.net/wms",
    "xmlns:xlink": "http://www.w3.org/1999/xlink",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsi:schemaLocation": "http://www.opengis.net/wms http://schemas.opengis.net/wms/1.3.0/capabilities_1_3_0.xsd"
}

hostname = socket.gethostname()

PIL_TYPE_MAPPING = {'image/jpeg': 'jpeg', 'image/png': 'png', 'image/png8': 'png256'}

def GetCapabilities(serviceModel: Service, db: Session):
    root = ET.Element("WMS_Capabilities", attrib={"version": "1.3.0", **namespaces})
    
    # Service
    service = ET.SubElement(root, "Service")
    ET.SubElement(service, "Name").text = serviceModel.name
    ET.SubElement(service, "Title").text = serviceModel.title

    if serviceModel.abstract:
        ET.SubElement(service, "Abstract").text = serviceModel.abstract

    if serviceModel.keywords:
        ET.SubElement(service, "Keywords").text =  serviceModel.keywords    

    ContactInformation = ET.SubElement(service, "ContactInformation")
    ContactPersonPrimary = ET.SubElement(ContactInformation, "ContactPersonPrimary")
    ContactPerson = ET.SubElement(ContactPersonPrimary, "ContactPerson")
    ContactOrganization = ET.SubElement(ContactPersonPrimary, "ContactOrganization")
    ContactPosition = ET.SubElement(ContactInformation, "ContactPosition")

    Fees = ET.SubElement(service, "Fees").text = "none"
    AccessConstraints = ET.SubElement(service, "AccessConstraints").text = "none"

    # Capability
    capability = ET.SubElement(root, "Capability")
    request = ET.SubElement(capability, "Request")    
    
    # GetCapabilities
    GetCapabilities = ET.SubElement(request, "GetCapabilities")
    ET.SubElement(GetCapabilities, "Format").text = "text/xml"
    createDCPType(GetCapabilities, [
        { "tag": "GET", "resource": "http://localhost:8080/geoserver/ows?SERVICE=WMS&amp;" }        
    ])

    OnlineResource = ET.SubElement(service, "OnlineResource", 
        attrib= { 
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "xlink:type": "simple",
            "xlink:href": f"http://{hostname}"
        }
    )

    GetMapFormats = get_map_formats(db)
    # GetMapFormats = [obj["format"] for obj in GetMapFormats]

    # GetMapFormats = ["image/png", "application/atom+xml", "application/json;type=geojson", "application/json;type=topojson",
    #                  "application/json;type=utfgrid", "application/pdf", "application/rss+xml"]
    
    # GetMap
    GetMap = ET.SubElement(request, "GetMap")
    
    for format in GetMapFormats:
        createFormat(GetMap, format)

    GetMapResources = [
        { "tag": "GET", "resource": "http://localhost:8080/geoserver/ows?SERVICE=WMS&" }        
    ]
    createDCPType(GetMap, GetMapResources)

    # GetFeatureInfo
    GetFeatureInfo = ET.SubElement(request, "GetFeatureInfo")

    GetFeatureInfoFormats = ["text/plain", "application/vnd.ogc.gml", "text/xml", "application/vnd.ogc.gml/3.1.1",]
    for format in GetFeatureInfoFormats:
        createFormat(GetFeatureInfo, format)

    GetFeatureResources = [
        { "tag": "GET", "resource": "http://localhost:8080/geoserver/ows?SERVICE=WMS&" }        
    ]

    createDCPType(GetFeatureInfo, GetFeatureResources)

    createException(capability)

    createLayer(capability, db)

    # Use ElementTree to include the XML declaration
    tree = ET.ElementTree(root)
    xml_output = io.BytesIO()
    tree.write(xml_output, encoding="utf-8", xml_declaration=True)

    # Convert to string and return
    return xml_output.getvalue().decode("utf-8")

def GetMap(geotiff_path, bbox, width, height, crs, format="image/png"):
    return WMSBaseServiceHandle.GetMap(geotiff_path, bbox, width, height, crs, format=format)

# def GetMap(geotiff_path, bbox, width, height, crs, format="image/png"):
#     """
#     Generate a WMS GetMap response from a GeoTIFF.

#     Args:
#         geotiff_path (str): Path to the GeoTIFF file.
#         bbox (tuple): Bounding box (minx, miny, maxx, maxy) in the requested CRS.
#         width (int): Width of the output image.
#         height (int): Height of the output image.
#         crs (str): Requested CRS (e.g., "EPSG:4326").
#         format (str): Output format (e.g., "image/png").

#     Returns:
#         bytes: The generated image bytes.
#     """
#     # TODO: Validate CRS
    

#     # Validate if the GeoTIFF is a valid COG
#     if not cog_validate(geotiff_path):
#         raise ValueError("The provided GeoTIFF is not a valid Cloud Optimized GeoTIFF.")

#     with rasterio.open(geotiff_path) as src:
#         # Convert bounding box to the GeoTIFF CRS
#         if not src.transform or src.transform == Affine.identity():
#             print("No geotransform found. Using default transform.")
#             transform = Affine.translation(0, 0) * Affine.scale(1, -1)  # Identity transform
#         else:
#             transform = src.transform

#         print(transform)
#         src_crs = src.crs

#         print(src_crs)
        
#         # Convert string to tuple of floats
#         bbox = tuple(map(float, bbox.split(",")))

#         # Reproject bounding box if CRS differs
#         if crs != str(src_crs):
#             from pyproj import Transformer
#             transformer = Transformer.from_crs(crs, src_crs, always_xy=True)
#             bbox = transformer.transform_bounds(*bbox)
        
#         # Create a window for the requested bounding box
#         window = from_bounds(*bbox, transform=src.transform)
        
#         # Read the raster data within the window
#         data = src.read(window=window, out_shape=(src.count, height, width))
#         print(data)

#         # Normalize to 8-bit and convert to PNG
#         normalized_data = (data / data.max() * 255).astype("uint8")
#         print(normalized_data)
        
#         if format is "image/jpg":
#             driver = "JPG"
#         else:
#             driver = "PNG"
        
#         # Write to PNG using Pillow
#         with MemoryFile() as memfile:
#             with memfile.open(driver=driver, width=width, height=height, count=src.count, dtype="uint8") as dst:
#                 dst.write(normalized_data)
#             png_data = memfile.read()
                
#         return png_data

def GetFeatureInfo(self, params):
    
    return ""

    

def createOnlineResource(parent: ET.Element, tag: str, resource: str):
    subElement = ET.SubElement(parent, tag)
    OnlineResource = ET.SubElement(subElement, "OnlineResource", attrib={ "xlink:type": "simple", "xlink:href": resource })
    return OnlineResource

def createDCPType(parent: ET.Element, resources):
    DCPType = ET.SubElement(parent, "DCPType")
    HTTP = ET.SubElement(DCPType, "HTTP")    

    for resource in resources:        
        createOnlineResource(HTTP, tag=resource['tag'], resource=resource['resource'])
    
    return DCPType

def createFormat(parent: ET.Element, text: str): 
    element = ET.SubElement(parent, "Format").text = text
    return element

def createException(parent: ET.Element):
    Exception = ET.SubElement(parent, "Exception")
    createFormat(Exception, "XML")
    createFormat(Exception, "INIMAGE")
    createFormat(Exception, "BLANK")
    createFormat(Exception, "JSON")
    createFormat(Exception, "JSONP")

def createLayer(parent: ET.Element, db: Session):
    layer = ET.SubElement(parent, "Layer")
    name = ET.SubElement(layer, "Name")
    title = ET.SubElement(layer, "Title")
    abstract = ET.SubElement(layer, "Abstract")

    # CRS
    crs_list = ["AUTO:42001", "EPSG:2000"]
    for crs in crs_list:
        ET.SubElement(layer, "CRS").text = crs

    # EX_GeographicBoundingBox = ET.SubElement(layer, "EX_GeographicBoundingBox")
    # ET.SubElement(EX_GeographicBoundingBox, "westBoundLongitude").text = "100.6238350820671"
    # ET.SubElement(EX_GeographicBoundingBox, "eastBoundLongitude").text = "102.91331158996276"
    # ET.SubElement(EX_GeographicBoundingBox, "southBoundLatitude").text = "2.8201217928695064"
    # ET.SubElement(EX_GeographicBoundingBox, "northBoundLatitude").text = "5.558142856024738"

    # createBoundingBox(layer, "CRS:84", "100.6238350820671", "2.8201217928695064", "102.91331158996276", "5.558142856024738")

    # # Create Layer
    layers = get_layers(db)    

    # for loop layers
    for single_layer in layers:
        print(single_layer.name)        
        createSingleLayer(layer, single_layer)


def createBoundingBox(parent: ET.Element, crs: str, minx: str, miny: str, maxx: str, maxy: str):
    ET.SubElement(parent, "BoundingBox", { "crs": crs, "minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy })    

def createEx_GeographicBoundingBox(parent: ET.Element, west_bound_longitude: float, east_bound_longitude: float,
                                   south_bound_latitude: float, north_bound_latitude: float):
    EX_GeographicBoundingBox = ET.SubElement(parent, "EX_GeographicBoundingBox")
    ET.SubElement(EX_GeographicBoundingBox, "westBoundLongitude").text = west_bound_longitude
    ET.SubElement(EX_GeographicBoundingBox, "eastBoundLongitude").text = east_bound_longitude
    ET.SubElement(EX_GeographicBoundingBox, "southBoundLatitude").text = south_bound_latitude
    ET.SubElement(EX_GeographicBoundingBox, "northBoundLatitude").text = north_bound_latitude

def createSingleLayer(parent: ET.Element, layerModel: Layer):
    d = { 
        "queryable" : str(layerModel.queryable),
        "opaque" : str(layerModel.opaque)
    }    

    layer = ET.SubElement(parent, "Layer", attrib=d)
    name = ET.SubElement(layer, "Name").text = layerModel.name
    title = ET.SubElement(layer, "Title").text = layerModel.title
    abstract = ET.SubElement(layer, "Abstract").text = layerModel.abstract
        
    keywordList =  ET.SubElement(layer, "KeywordList")
    # for loop keywords    
    for keyword in layerModel.keywords:
        ET.SubElement(keywordList, "keyword").text = keyword.keyword

    # CRS    
    for crs in layerModel.crss:
        ET.SubElement(layer, "CRS").text = crs.crs


    createEx_GeographicBoundingBox(layer, layerModel.west_bound_longitude, 
                                   layerModel.east_bound_longitude, layerModel.south_bound_latitude,
                                   layerModel.north_bound_latitude)