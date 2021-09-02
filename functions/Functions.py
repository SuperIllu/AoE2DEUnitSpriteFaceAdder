import tkinter

import PIL
from PIL import Image, ImageTk


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


def loadImageToCanvas(imagePreview: Image, canvas: tkinter.Canvas, resample=None):
    """ does not resize the original image, returns the resized one """
    if imagePreview:
        try:
            canvasSize = getCanvasSize(canvas)
            targetImageSize = calculatePreviewImageSize(canvasSize, imagePreview)
            imagePreview = imagePreview.copy()
            imagePreview = imagePreview.resize(targetImageSize, resample=resample)  # , PIL.Image.NEAREST = exact pixel scaling
            photoImagePreview = ImageTk.PhotoImage(imagePreview)
            padding = calculatePadding(canvasSize, targetImageSize)
            canvas.create_image(padding[0], padding[1], anchor="nw", image=photoImagePreview)
            return (imagePreview, photoImagePreview)
        except Exception as e:
            print(e)
    else:
        canvas.config(bg="grey")
    return (None, None)


def loadImagePathToCanvas(fullImagePath: str, canvas: tkinter.Canvas):
    if fullImagePath:
        try:
            print(f"Preview image: {fullImagePath}")
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