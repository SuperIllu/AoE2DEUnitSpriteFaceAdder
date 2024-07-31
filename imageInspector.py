import tkinter as tk

import PIL
from PIL import Image
from functions.Functions import loadImageToCanvas, calculatePreviewImageSize, getCanvasSize


def link_image_inspector(element, image: Image, image_name: str, on_closed_callback=None):
    element.bind("<Button-2>", lambda event: ImageInspector(image, image_name, on_closed_callback))


class ImageInspector:

    def __init__(self, image: Image, image_name: str, on_closed_callback):
        self._image = image
        self._image_name = image_name
        self._pixels = image.load()
        self._on_closed_callback = on_closed_callback

        self._main = tk.Toplevel()
        self._main.title(f"Inspector: {image_name}")
        self._main.grid_rowconfigure(0, weight=1)
        self._main.grid_rowconfigure(1, weight=0)
        self._main.grid_columnconfigure(0, weight=1)

        self._canvas = tk.Canvas(self._main, width=600, height=600)
        target_size = calculatePreviewImageSize(getCanvasSize(self._canvas), image)
        self._canvas.config(width=target_size[0], height=target_size[1])
        self._resized_image, self._resized_photoimage = loadImageToCanvas(self._image, self._canvas,
                                                                          resample=PIL.Image.NEAREST)
        self._scaled_pixels = self._resized_image.load()

        self._canvas.bind("<Motion>", self._evaluate_mouse_position)
        self._colourVar = tk.StringVar()
        colour_label = tk.Label(self._main, textvariable=self._colourVar)
        self._position_var = tk.StringVar()
        position_label = tk.Label(self._main, textvariable=self._position_var)

        self._canvas.grid(row=0, column=0)
        colour_label.grid(row=1, column=0)
        position_label.grid(row=2, column=0)

        self._main.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        self._main.destroy()
        if self._on_closed_callback:
            self._on_closed_callback()

    def _evaluate_mouse_position(self, event):
        self._position_var.set(f"Position {event.x} / {event.y}")
        if 0 <= event.x < self._resized_image.size[0] and 0 <= event.y < self._resized_image.size[1]:
            self._colourVar.set(f"Colour {self._scaled_pixels[event.x, event.y]}")
        else:
            self._colourVar.set("Colour: pixel out of range")
