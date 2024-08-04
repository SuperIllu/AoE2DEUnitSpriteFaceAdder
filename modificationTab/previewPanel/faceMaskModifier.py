from __future__ import annotations

import math
import tkinter as tk
from itertools import product

import PIL
from PIL import Image

from functions.Functions import calculatePreviewImageSize, loadImageToCanvas, getCanvasSize, timeit
from functions.faceMaskUtils import mark_subtracted_images, highlight_pixels, FaceMaskConfig, bytes_to_face_mask
from managers.imageConfigManager import ImageConfiguration


class FaceMaskModifier:
    """
    This class shows the zoomed in view of the mask which can be applied to face/head sprites
    and is used to modify the mask, i.e. choose which pixels of the face/head sprite should be used.
    """
    _instance = None
    Visible_pixel = 255  # white in grey scale
    Hidden_pixel = 0  # black in grey scale

    def __init__(self):
        # need to cache the images we show, otherwise they disappear
        self._resizedPhotomage = None
        self._resizedImage = None

        self._face_mask_pixels = None
        self._face_mask = None

        self._face_image = None
        self._face_pixels = None

        self._last_mapped_pixel_under_mouse = None
        self._on_masked_changed = None
        self._buildUI()

    @classmethod
    def get_instance(cls) -> FaceMaskModifier:
        """ creates and instance if necessary, or returns the existing one """
        if cls._instance is None:
            cls._instance = FaceMaskModifier()
        return cls._instance

    @classmethod
    def check_and_get(cls) -> FaceMaskModifier:
        """ only gets the reference, does not create one"""
        return cls._instance


    def _buildUI(self):
        self._main = tk.Toplevel()
        self._main.title(f"Face mask modifier")
        self._main.grid_rowconfigure(0, weight=1)
        self._main.grid_rowconfigure(1, weight=0)
        self._main.grid_rowconfigure(2, weight=0)
        self._main.grid_columnconfigure(0, weight=1)
        self._main.grid_columnconfigure(1, weight=1)

        self._canvas = tk.Canvas(self._main, width=400, height=400)
        self._canvas.bind("<Motion>", self._evaluateMousePosition)
        self._canvas.bind("<Button-1>", self._mouse_position_clicked)
        self._canvas.bind("<ButtonRelease-1>", self._mouse_button_released)
        self._canvas.bind("<Leave>", self._mouse_left)
        self._colourVar = tk.StringVar()
        colour_label = tk.Label(self._main, textvariable=self._colourVar)
        self._positionVar = tk.StringVar()
        position_label = tk.Label(self._main, textvariable=self._positionVar)

        mode_frame = tk.Frame(self._main)
        brush_size_label = tk.Label(mode_frame, text="Brush size")
        self._brush_size_var = tk.StringVar()
        brush_size_options= [
            "1x1",
            "2x2",
            "3x3",
            "4x4",
            "5x5",
        ]
        self._brush_size_var.set(brush_size_options[0])
        self._update_brush_size(None)

        brush_size_dropdown = tk.OptionMenu(mode_frame, self._brush_size_var, *brush_size_options,
                                            command=self._update_brush_size)
        brush_mode_label = tk.Label(mode_frame, text="Mode:")
        self._brush_mode_var = tk.StringVar()
        self._brush_mode_label = tk.Label(mode_frame, textvariable=self._brush_mode_var)
        self._set_brush_mode("auto")

        brush_size_label.grid(row=0, column=0, sticky="e", padx=(5, 5))
        brush_size_dropdown.grid(row=0, column=1, sticky="e", padx=(5, 5))
        brush_mode_label.grid(row=0, column=2, sticky="e", padx=(5, 5))
        self._brush_mode_label.grid(row=0, column=3, sticky="e", padx=(5, 5))

        self._canvas.grid(row=0, column=0, columnspan=2)
        colour_label.grid(row=1, column=0, padx=(20, 10), sticky="w")
        position_label.grid(row=1, column=1, padx=(10, 20), sticky="e")
        mode_frame.grid(row=2, column=0, columnspan=2)

        self._main.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        FaceMaskModifier._instance = None
        self._main.destroy()

    def _update_brush_size(self, event):
        self._brush_size = int(self._brush_size_var.get()[0])

    def _mouse_left(self, event):
        self._set_brush_mode("auto")
        self._on_masked_changed(self._face_mask)

    def _mouse_button_released(self, event):
        self._set_brush_mode("auto")
        self._on_masked_changed(self._face_mask)

    def _set_brush_mode(self, mode: str):
        if mode == "auto":
            self._brush_mode_var.set("auto")
            self._brush_mode_label.config(background="white")
        elif mode == "mask":
            self._brush_mode_var.set("mask")
            self._brush_mode_label.config(background="light green")
        elif mode == "unmask":
            self._brush_mode_var.set("unmask")
            self._brush_mode_label.config(background="yellow")
        else:
            raise Exception(f"un-supported mode: {mode}")

    #@timeit
    def _evaluateMousePosition(self, event):
        if self._face_image is None:
            return

        # scaling is uniform, both in x and y
        scaling = self._resizedImage.size[0] / self._face_image.size[0]
        # get back from scaled pixels to original size
        mapped_pixel = self._get_mapped_pixel((event.x, event.y))
        if self._last_mapped_pixel_under_mouse == mapped_pixel:
            return
        self._last_mapped_pixel_under_mouse = mapped_pixel
        # (math.floor(event.x / scaling), math.floor(event.y / scaling))

        self._positionVar.set(f"Position {event.x} / {event.y} ({mapped_pixel})")
        if 0 <= event.x < self._resizedImage.size[0] and 0 <= event.y < self._resizedImage.size[1]:
            self._colourVar.set(f"Colour {self._scaledPixels[event.x, event.y]}")
        else:
            self._colourVar.set("Colour: pixel out of range")
            return

        if self._brush_mode_var.get() == "mask":
            self._set_pixels(mapped_pixel, FaceMaskModifier.Hidden_pixel)
            self._update_image_visuals()
        elif self._brush_mode_var.get() == "unmask":
            self._set_pixels(mapped_pixel, FaceMaskModifier.Visible_pixel)
            self._update_image_visuals()

        # ALWAYS update visuals

        highlight_pixels(self._canvas, mapped_pixel, scaling, self._brush_size)

    def _get_mapped_pixel(self, position):
        return tuple(math.floor(x / self._scaling) for x in position)


    def _set_pixels(self, unscaled_position, outcome):
        """ mark selected pixels as hidden/visible, based on position and brush size """
        x_range = range(0, self._brush_size)
        y_range = range(0, self._brush_size)
        for (x, y) in product(x_range, y_range):
            if self._face_pixels[unscaled_position][-1] == 0:
                # skip transparent pixels
                continue
            internal_position = tuple((px + py) for (px, py) in zip((x, y), unscaled_position))
            if internal_position[0] >= self._face_image.size[0] or internal_position[1] >= self._face_image.size[1]:
                continue
            self._face_mask_pixels[internal_position] = outcome

    #@timeit
    def _update_image_visuals(self):
        marked_image = mark_subtracted_images(self._face_image, self._face_mask, self._scaling)
        self._resizedImage, self._resizedPhotomage = loadImageToCanvas(marked_image, self._canvas,
                                                                       resample=PIL.Image.NEAREST)

    def _mouse_position_clicked(self, event):
        # the colour values on the face mask

        # get back from scaled pixels to original size as we don't need individual info on pixels within scaled pixels
        mapped_pixel = self._get_mapped_pixel((event.x, event.y))

        # toggle between visible and invisible:
        if self._face_mask_pixels[mapped_pixel] == FaceMaskModifier.Visible_pixel:
            # clicked on visible pixel -> start masking
            self._set_brush_mode("mask")
            self._set_pixels(mapped_pixel, FaceMaskModifier.Hidden_pixel)
        elif self._face_mask_pixels[mapped_pixel] == FaceMaskModifier.Hidden_pixel:
            # clicked on (already) masked pixel -> start unmasking
            self._set_brush_mode("unmask")
            self._set_pixels(mapped_pixel, FaceMaskModifier.Visible_pixel)
        else:
            print(f"Wrong pixel colour: {self._face_mask_pixels[mapped_pixel]}")

        # update visuals
        self._update_image_visuals()

    def load_mask(self, image: Image, config: ImageConfiguration, on_mask_changed):
        assert self._canvas and self._canvas.winfo_exists(), "canvas is gone"

        self._config = config
        self._on_masked_changed = on_mask_changed
        self._face_image = image
        self._face_pixels = image.load()
        self._canvas.configure(width=400, height=400)

        target_size = calculatePreviewImageSize((400, 400), image)
        self._canvas.config(width=target_size[0], height=target_size[1])
        # do one initial load to get the resized image, needed to determine the scaling
        self._resizedImage, self._resizedPhotomage = loadImageToCanvas(self._face_image, self._canvas,
                                                                       resample=PIL.Image.Resampling.NEAREST)
        self._scaledPixels = self._resizedImage.load()

        # scaling is uniform, both in x and y
        self._scaling = self._resizedImage.size[0] / self._face_image.size[0]
        self.update_visuals()

    def update_visuals(self):
        config = self._config.faceMask
        if config and config.mask_image:
            self._face_mask = bytes_to_face_mask((config.dx, config.dy), config.mask_image)
            self._update_image_visuals()
        else:
            # no mask created yet
            self._face_mask = Image.new("L", self._face_image.size, 255)  # mask is in grey scale
            self._resizedImage, self._resizedPhotomage = loadImageToCanvas(self._face_image, self._canvas,
                                                                           resample=PIL.Image.Resampling.NEAREST)
        self._face_mask_pixels = self._face_mask.load()

