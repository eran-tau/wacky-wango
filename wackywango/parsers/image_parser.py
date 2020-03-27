from PIL import Image


def parse_snapshot(snap):
    image = Image.frombytes('RGB', (snap.color_image.width, snap.color_image.height), snap.color_image.data)
    return image