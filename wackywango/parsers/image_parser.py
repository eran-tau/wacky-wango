from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import uuid

def parse_color_image(snap):
    image = Image.frombytes('RGB', (snap.color_image.width, snap.color_image.height), snap.color_image.data)
    return image

def parse_depth_image(snap):
    size = snap.depth_image.height, snap.depth_image.width
    image_array = np.array(snap.depth_image.data).reshape(size)
    help = plt.imshow(image_array, cmap='hot')
    unique_filename = "pics/" + 'depth_image' + "/" + str(uuid.uuid4()) + ".jpg"
    plt.savefig(unique_filename)
    return help
