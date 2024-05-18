import base64
import uuid
from io import BytesIO
from PIL import Image

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered,format=image.format)
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return image_base64

def add_uuid_to_base64(image_base64):
    image_uuid = str(uuid.uuid4())
    return f"{image_base64}{image_uuid}"

def base64_to_image(image_base64_with_uuid):
    image_base64 = image_base64_with_uuid[:-36]
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))
    return(image)
def process_image(image):
    try:
        image_base64 = image_to_base64(image)
        image_base64_with_uuid = add_uuid_to_base64(image_base64)
        processed_image = base64_to_image(image_base64_with_uuid)
        return processed_image, image_base64, image_base64_with_uuid
    except Exception as e:
        return None, None, None
