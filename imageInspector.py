import tkinter as tk

import PIL
from PIL import Image
from functions.Functions import loadImageToCanvas, calculatePreviewImageSize, getCanvasSize


def linkImageInspector(element, image: Image, imageName: str):
    element.bind("<Button-2>", lambda event: ImageInspector(image, imageName))


class ImageInspector:

    def __init__(self, image: Image, imageName:str ):
        self._image = image
        self._imageName = imageName
        self._pixels = image.load()

        self._main = tk.Toplevel()
        self._main.title(f"Inspector: {imageName}")
        self._main.grid_rowconfigure(0, weight=1)
        self._main.grid_rowconfigure(1, weight=0)
        self._main.grid_columnconfigure(0, weight=1)

        self._canvas = tk.Canvas(self._main, width=600, height=600)
        targetSize = calculatePreviewImageSize(getCanvasSize(self._canvas), image)
        self._canvas.config(width=targetSize[0], height=targetSize[1])
        self._resizedImage, self._resizedPhotomage = loadImageToCanvas(self._image, self._canvas,
                                                                       resample=PIL.Image.NEAREST)
        self._scaledPixels = self._resizedImage.load()

        self._canvas.bind("<Motion>", self._evaluateMousePosition)
        self._colourVar = tk.StringVar()
        colourLabel = tk.Label(self._main, textvariable=self._colourVar)
        self._positionVar = tk.StringVar()
        positionLabel = tk.Label(self._main, textvariable=self._positionVar)

        self._canvas.grid(row=0, column=0)
        colourLabel.grid(row=1, column=0)
        positionLabel.grid(row=2, column=0)


    def _evaluateMousePosition(self, event):
        self._positionVar.set(f"Position {event.x} / {event.y}")
        if 0 <= event.x < self._resizedImage.size[0] and 0 <= event.y < self._resizedImage.size[1]:
            self._colourVar.set(f"Colour {self._scaledPixels[event.x, event.y]}")
        else:
            self._colourVar.set("Colour: pixel out of range")
