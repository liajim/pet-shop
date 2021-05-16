from io import BytesIO
from os.path import split, splitext

import numpy as np
from PIL import Image


def represents_float(float_str):
    float_str = float_str.replace(',', '.')
    try:
        float(float_str)
        return True
    except:
        return False


def crop_according_content(image):
    image_data = np.array(image)
    image_data_bw = image_data.max(axis=2)
    non_empty_columns = np.where(image_data_bw.min(axis=0) < 255)[0]
    non_empty_rows = np.where(image_data_bw.min(axis=1) < 255)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))
    image_data_new = image_data[cropBox[0]:cropBox[1] + 1, cropBox[2]:cropBox[3] + 1]
    new_image = Image.fromarray(image_data_new)
    new_image.load()
    return new_image


def convert_to_buffer(img, format_str='JPEG'):
    if format_str.lower() == 'jpg':
        format_str = 'JPEG'
    buf = BytesIO()
    img.save(buf, format=format_str)
    return buf.getvalue()


def image_treatment(name, data):
    try:
        image_load = Image.open(BytesIO(data))
        image_load.load()
        image = Image.open(BytesIO(data))
        image.verify()
    except:
        return None
    name = split(name)[1]
    if splitext(name)[1].lower() == '.png':
        background = Image.new("RGB", image_load.size, (255, 255, 255))
        background.paste(image_load, mask=image_load.convert('RGBA').split()[3])
        image_load = background
    image_load = crop_according_content(image_load)
    data = convert_to_buffer(image_load)
    return data


def open_and_treat_image(img):
    name = img.name
    data = convert_to_buffer(Image.open(img), img.name.split('.')[1])
    return image_treatment(name, data)
