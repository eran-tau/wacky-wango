from PIL import Image


def parse_color_image(context, snap):
    image = Image.frombytes('RGB', (snap.color_image.width,
                                    snap.color_image.height),
                            snap.color_image.data)
    data = context.save(image)
    return data


parse_color_image.parser_type = 'color_image'
