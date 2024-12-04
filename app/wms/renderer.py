from PIL import Image, ImageDraw
import io

def render_map(layers: str, bbox: tuple, width: int, height: int, crs: str) -> bytes:
    """
    Render a map image for given parameters.
    """
    minx, miny, maxx, maxy = bbox
    layer_list = layers.split(",")
    
    # Create a blank image
    image = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # Example: Draw bounding box (you can replace this with real data rendering)
    draw.rectangle([(0, 0), (width, height)], outline="black")
    draw.text((10, 10), f"Layers: {', '.join(layer_list)}", fill="black")
    draw.text((10, 30), f"BBOX: {bbox}", fill="black")
    draw.text((10, 50), f"CRS: {crs}", fill="black")
    
    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    return img_bytes.getvalue()
