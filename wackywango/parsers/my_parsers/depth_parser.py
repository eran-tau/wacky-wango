import matplotlib.pyplot as plt
import numpy as np


def parse_depth_image(context, snap):
    size = snap.depth_image.height, snap.depth_image.width
    image_array = np.array(snap.depth_image.data).reshape(size)
    plt.imshow(image_array, cmap='hot')
    unique_filename = context.get_save_path()
    plt.savefig(unique_filename)
    return unique_filename


parse_depth_image.parser_type = 'depth_image'
