import os
from PIL import Image

def is_image(path):
    return os.path.exists(path) and (path.endswith(".png") or path.endswith(".jpg") or path.endswith(".jpeg")
                                     or path.endswith(".bmp") or path.endswith(".webp"))

def get_icon_path():
    return os.getcwd() + "\\icon.ico"

def get_icon():
    return Image.open(get_icon_path())