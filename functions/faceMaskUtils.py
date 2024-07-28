
"""
this class contains util functions to handle interactions between face sprites and the face
masks
"""
import base64
import dataclasses
import math
import tkinter
import zlib
from dataclasses import dataclass
from itertools import product
from math import floor
import numpy as np

from PIL import Image


# this class only exists to avoid circular imports with the face mask modifier class
class UtilConsts:
    Visible_pixel = 255  # white in grey scale
    Hidden_pixel = 0  # black in grey scale


@dataclass(order=True)
class FaceMaskConfig:
    use_mask: bool = False
    mirrored: bool = False
    dx: int = None
    dy: int = None
    mask_image: str = None

    def serialise(self):
        return dataclasses.asdict(self)


def face_mask_to_bytes(face_mask: Image) -> tuple:
    # Ensure the image is in 1-bit format (black and white)
    image = face_mask.convert('1')

    image_data = np.array(image)
    if np.all(image_data == 255):
        # All pixels are white -> same as no mask
        return (0, 0, "")
    else:
        # Convert image data to bytes
        image_bytes = np.packbits(image_data).tobytes()

        # Compress the byte data
        compressed_data = zlib.compress(image_bytes)

        # Convert compressed data to base64 string for JSON storage
        encoded_data = base64.b64encode(compressed_data).decode('utf-8')

    return (image.size, encoded_data)


def bytes_to_face_mask(dimensions, data: str) -> Image:
    if data == "":
        # All pixels are white, create an all-white image
        image_array = np.ones(dimensions, dtype=np.uint8) * 255
    else:
        # Decode the base64 string and decompress the data
        compressed_data = base64.b64decode(data)
        decompressed_data = zlib.decompress(compressed_data)

        # Convert byte data back to image
        image_array = np.unpackbits(np.frombuffer(decompressed_data, dtype=np.uint8))
        image_array = image_array[:dimensions[0] * dimensions[1]].reshape(dimensions) * 255

    # Create a PIL image from the array
    image = Image.fromarray(image_array, mode='L').convert('1')
    return image


def apply_face_mask_mods(face_image: Image, config, ignore_on: bool = False) -> Image:
    # TODO mirroring currently not supported
    if config.faceMask is None or not config.faceMask.mask_image:
        # mask exists
        return face_image
    if not (config.faceMask.use_mask or ignore_on):
        # mask should be shown
        return face_image
    dimensions = (config.faceMask.dx, config.faceMask.dy)
    mask_image = bytes_to_face_mask(dimensions, config.faceMask.mask_image)
    return subtract_images(face_image, mask_image)


def subtract_images(image: Image, mask: Image) -> Image:
    """
    Takes in an image and its mask and returns a new image where the mask pixels have been removed form the image
    :param image:
    :param mask:
    :return:
    """
    if image.size != mask.size:
        raise f"Image.size({image.size}) != Mask.size({mask.size})"

    output_image = Image.new("RGBA", image.size, (225, 225, 225, 0))

    image_pixels = image.load()
    mask_pixels = mask.load()
    output_pixels = output_image.load()

    for (x, y) in product(range(image.size[0]), range(image.size[1])):
        if mask_pixels[x, y] == UtilConsts.Visible_pixel:
            output_pixels[x, y] = image_pixels[x, y]
#        else:
#            output_pixels[x, y] = trans_colour

    return output_image


def is_even(x):
    return x % 2 == 0


def _should_be_red(x, y):
    return (x + y) % 8 == 0


def add_image_pixels(output_pixels, image_pixels, position: tuple, scale_factor):
    """ this functions handles the multiple pixels for each upscale pixel
        just adds the original pixels of the image onto the output
    """
    x_range = range(0, scale_factor)
    y_range = range(0, scale_factor)
    for pixel_index in product(x_range, y_range):
        global_pixel_index = (position[0] * scale_factor + pixel_index[0], position[1] * scale_factor + pixel_index[1])
        output_pixels[global_pixel_index] = image_pixels[position]


def add_masked_image_pixels(output_pixels, image_pixels, position, scale_factor):
    """ this functions handles the multiple pixels for each upscale pixel
        adds a modified version of the pixel onto the ouput to indicate that is has been masked
    """
    mask_colour = (255, 0, 0)  # red dots indicating the pixel behing hidden

    x_range = range(0, scale_factor)
    y_range = range(0, scale_factor)
    for pixel_index in product(x_range, y_range):
        if image_pixels[position][-1] == 0:
            # skip transparent pixels for performance reasons
            continue
        global_pixel_index = (position[0] * scale_factor + pixel_index[0], position[1] * scale_factor + pixel_index[1])
        if _should_be_red(pixel_index[0], pixel_index[1]):
            output_pixels[global_pixel_index] = mask_colour
        else:
            output_pixels[global_pixel_index] = image_pixels[position]


def mark_subtracted_images(face_image: Image, mask: Image, scaling: int) -> Image:
    """
    this takes an **unscaled** image and **unscaled** mask and marks its images with a certain
     colour to show that they will be masked
    :param face_image:
    :param mask:
    :return:
    """
    scaling = int(scaling)

    if scaling <= 1:
        raise Exception(f"Image not up-scaled at all (f={scaling})")

    # the colour in the mask indicating that this pixel should be hidden
    # here it shows that this pixel should be marked
    mask_colour = (0, 0, 0)

    scaled_image_size = (int(face_image.size[0] * scaling), int(face_image.size[1] * scaling))
    # needs to contain alpha as some face sprites have weird alpha values (black and white pixels with a=0)
    output_image = Image.new("RGBA", scaled_image_size, (255, 255, 255, 0))

    image_pixels = face_image.load()
    mask_pixels = mask.load()
    output_pixels = output_image.load()

    x_range = range(0, int(face_image.size[0]))
    y_range = range(0, int(face_image.size[1]))

    # go through the original number of pixels without upscaling
    for (x, y) in product(x_range, y_range):
        if mask_pixels[x, y] != UtilConsts.Hidden_pixel:
            # just add the same pixels as in the original image
            add_image_pixels(output_pixels, image_pixels, (x, y), scaling)
        else:
            # add pixels that show that this up-scaled pixel is masked
            add_masked_image_pixels(output_pixels, image_pixels, (x, y), scaling)

    return output_image


def highlight_pixels(image: tkinter.Canvas, position: tuple, scaling: int, highlight_size: int):
    scaled_position = tuple(x * scaling for x in position)
    scaled_end_pos = tuple((x + highlight_size) * scaling for x in position)
    image.delete("highlight")
    image.create_rectangle(scaled_position, scaled_end_pos, outline="blue", tags="highlight")
