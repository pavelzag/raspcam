import io
import string
from google.cloud import vision
from google.cloud.vision import types


def detect_text(file_name):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    for text in texts:
        print('\n"{}"'.format(text.description))
    voltage = values_builder(texts, 'voltage')
    current = values_builder(texts, 'current')
    charge_amt = values_builder(texts, 'charge_amt')
    return voltage, current, charge_amt


def values_builder(texts, value_type):
    if value_type == 'voltage':
        voltage = texts[1].description + texts[2].description
        return string.replace(voltage, 'U', 'V')
    elif value_type == 'current':
        current_str = texts[4].description.split("-")[-2]
        return current_str
    elif value_type == 'charge_amt':
        charge_amt = '{}{}'.format('-', texts[4].description.split("-")[1])
        return charge_amt
