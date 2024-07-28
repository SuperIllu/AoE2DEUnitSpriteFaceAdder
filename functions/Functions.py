import tkinter
import time
from itertools import product
from functools import wraps

from PIL import Image, ImageTk


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        if total_time > 0.005:
            print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

def getCanvasSize(canvas) -> tuple[int, int]:
    canvasWidth = int(canvas["width"])
    canvasHeight = int(canvas["height"])
    return (canvasWidth, canvasHeight)


def calculatePreviewImageSize(canvasSize, previewImage) -> tuple[int, int]:
    picWidth = int(previewImage.width)
    picHeight = int(previewImage.height)
    widthRatio = canvasSize[0] / picWidth
    heightRatio = canvasSize[1] / picHeight
    scaleFactor = min(widthRatio, heightRatio)
    return int(picWidth * scaleFactor), int(picHeight * scaleFactor)


@timeit
def loadImageToCanvas(imagePreview: Image, canvas: tkinter.Canvas, resample=None):
    """ does not resize the original image, returns a resized copy """
    if imagePreview:
        try:
            _start = time.time()
            canvas.delete("_image_")
            canvasSize = getCanvasSize(canvas)
            targetImageSize = calculatePreviewImageSize(canvasSize, imagePreview)
            _s1 = time.time() #- _start
            imagePreview = imagePreview.copy()
            imagePreview = imagePreview.resize(targetImageSize, resample=resample)  # , PIL.Image.NEAREST = exact pixel scaling
            _s2 = time.time() #- _s1
            photoImagePreview = ImageTk.PhotoImage(imagePreview)
            padding = calculatePadding(canvasSize, targetImageSize)
            _s3 = time.time() #- _s2
            canvas.create_image(padding[0], padding[1], anchor="nw", image=photoImagePreview, tags="_image_")
            _s4 = time.time() #- _s3
            # print(f"s1: {_s1 - _start}, s2: {_s2 - _s1}, s3: {_s3 - _s2}, s4: {_s4 - _s3}")
            return (imagePreview, photoImagePreview)
        except Exception as e:
            print(e)
    else:
        canvas.config(bg="grey")
    return (None, None)


def loadImagePathToCanvas(fullImagePath: str, canvas: tkinter.Canvas):
    if fullImagePath:
        try:
            imagePreview = Image.open(fullImagePath)
            return loadImageToCanvas(imagePreview, canvas)
        except Exception as e:
            print(e)
    else:
        canvas.config(bg="grey")
    return (None, None)


def calculatePadding(canvasSize, targetImageSize) -> tuple[int, int]:
    """ creates padding to center an Image in a canvas """
    xSlack = canvasSize[0] - targetImageSize[0]
    ySlack = canvasSize[1] - targetImageSize[1]
    xPadding = int(xSlack/2)
    yPadding = int(ySlack/2)
    return (xPadding, yPadding)


def trimStringToElementLength(text: str, maxLength: int = 80) -> str:
    if not text:
        return "N/A"
    if len(text) > maxLength:
        return f"...{text[-maxLength:]}"
    return text


def print_image_pixels(image: Image):
    pixels = image.load()
    x_range = range(0, int(image.size[0]))
    y_range = range(0, int(image.size[1]))
    for (x, y) in product(x_range, y_range):
        print(f"{(x, y)}: {pixels[x, y]}")
