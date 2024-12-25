import xml.etree.ElementTree as ET
import io

from .common import WMSBaseServiceHandle

def generate_xml_response():
    # Define the namespaces and attributes
    namespaces = {
        "xmlns": "http://www.opengis.net/wms",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://www.opengis.net/wms http://schemas.opengis.net/wms/1.3.0/capabilities_1_3_0.xsd"
    }

    root = ET.Element("WMS_Capabilities", attrib={"version": "1.3.0", **namespaces})
    service = ET.SubElement(root, "Service")
    ET.SubElement(service, "Name").text = "WMS"
    ET.SubElement(service, "Title").text = "Example WMS Service"
    ET.SubElement(service, "Abstract").text = "This is an example WMS API."
    ET.SubElement(service, "Keywords").text =  "This is keywords."

    capability = ET.SubElement(root, "Capability")
    request = ET.SubElement(capability, "Request")
    map = ET.SubElement(request, "Map")
    capabilities = ET.SubElement(request, "Capabilities")
    # ET.SubElement(capability, request)

    # Use ElementTree to include the XML declaration
    tree = ET.ElementTree(root)
    xml_output = io.BytesIO()
    tree.write(xml_output, encoding="utf-8", xml_declaration=True)

    # Convert to string and return
    return xml_output.getvalue().decode("utf-8")

def GetCapabilities(self, params):
    return ""

def GetMap(geotiff_path, bbox, width, height, crs, format="image/png"):
    return WMSBaseServiceHandle.GetMap(geotiff_path, bbox, width, height, crs, format=format)

def GetFeatureInfo(self, params):
    return ""