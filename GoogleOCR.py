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
    print('{} {}'.format('Amount of values in returning list:', len(texts)))
    whole = values_builder(texts)
    # voltage = values_builder(texts, 'voltage')
    # current = values_builder(texts, 'current')
    # charge_amt = values_builder(texts, 'charge_amt')
    # return voltage, current, charge_amt
    return whole


def values_builder(texts, value_type=None):
    if not value_type:
        try:
            string_before = texts[0].description
            return string_before.replace('\n', ' ').replace('CH:4', '').replace('CH 4', '').replace('U', 'V')
        except:
            return 'Too dark to calculates'
    if value_type == 'voltage':
        # voltage = texts[1].description + texts[2].description
        voltage = texts[2].description
        return string.replace(voltage, 'U', 'V')
    elif value_type == 'current':
        current_str = texts[5].description.split("-")[-2]
        return current_str
    elif value_type == 'charge_amt':
        charge_amt = '{}{}'.format('-', texts[5].description.split("-")[1])
        return charge_amt
