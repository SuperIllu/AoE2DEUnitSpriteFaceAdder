import tkinter as tk

import PIL
from PIL import Image

from functions.Functions import loadImageToCanvas
from functions.faceMaskUtils import subtract_images, face_mask_to_bytes, FaceMaskConfig, apply_face_mask_mods
from managers.imageConfigManager import ImageConfiguration
from modificationTab.previewPanel.faceMaskModifier import FaceMaskModifier
from modificationTab.previewPanel.previewPanelUI import PreviewPanelUI
from idlelib.tooltip import Hovertip


class FaceModificationPanel:
    """
    Shows the preview of the face mask with its modifications and enables the user to modify it or
    remove all modifications
    """

    def __init__(self, master: PreviewPanelUI, on_mask_changed_callback):
        self._previewPanel = master
        self._update_merged_preview = on_mask_changed_callback
        self._raw_face = None
        self._face_modifier = None
        self._build()

    def _build(self):
        self._faceMaskPanel = tk.Frame(self._previewPanel.getFrame())
        self._faceMaskPanel.grid_columnconfigure(0, weight=1)

        self._useFaceMaskVar = tk.BooleanVar()
        self._flipImageVar = tk.BooleanVar()

        def _on_checkbox_toggled():
            print(f"toggled: {self._useFaceMaskVar.get()}")
            if self._config.faceMask is None:
                self._config.faceMask = FaceMaskConfig()
            self._config.faceMask.use_mask = self._useFaceMaskVar.get()
            self._update_merged_preview()

        faceMaskLabel = tk.Label(self._faceMaskPanel, text="Face mask")
        faceMaskCheckbox = tk.Checkbutton(self._faceMaskPanel, text="Use face mask",
                                          variable=self._useFaceMaskVar,
                                          command=_on_checkbox_toggled)
        flipFaceCheckbox = tk.Checkbutton(self._faceMaskPanel, text="Mirror image",
                                            variable=self._flipImageVar,
                                            command=lambda: print("togglee flip"))
        flipFaceCheckbox.config(state=tk.DISABLED)  # TODO mirroring currently not supported
        self._faceMaskCanvas = tk.Canvas(self._faceMaskPanel, bg="white",
                                             width=PreviewPanelUI.PreviewWidth,
                                             height=PreviewPanelUI.PreviewHeight)
        faceMaskResetButton = tk.Button(self._faceMaskPanel, text="Reset",
                                        command=self._resetMask)

        Hovertip(faceMaskCheckbox, "Will only save mask if this is checked")
        Hovertip(self._faceMaskCanvas, "Click to modify")

        faceMaskLabel.grid(row=0, column=0)
        faceMaskCheckbox.grid(row=1, column=0)
        flipFaceCheckbox.grid(row=2, column=0)
        self._faceMaskCanvas.grid(row=3, column=0)
        faceMaskResetButton.grid(row=4, column=0)

        def _loadModPanel() -> None:
            if self._raw_face is None:
                return
            self._useFaceMaskVar.set(True)
            self._face_modifier = FaceMaskModifier.get_instance()
            self._face_modifier.load_mask(self._raw_face, self._config, self._on_face_mask_changed)

        self._faceMaskCanvas.bind("<Button-1>", lambda e:  _loadModPanel())

        # place on parent frame, make sure to check the #column if this looks funky
        self._faceMaskPanel.grid(row=0, column=4, rowspan=4, sticky="ns")

    def _on_face_mask_changed(self, face_mask):
        face_mask_as_bytes = face_mask_to_bytes(face_mask)

        face_mask_config = FaceMaskConfig()
        face_mask_config.use_mask = self._useFaceMaskVar.get()
        face_mask_config.dx, face_mask_config.dy = face_mask_as_bytes[0]
        face_mask_config.mask_image = face_mask_as_bytes[1]
        self._config.faceMask = face_mask_config

        face_after_mask = subtract_images(self._raw_face, face_mask)
        self._update_face_preview()
        self._update_merged_preview()

    def _resetMask(self):
        self._config.faceMask = None
        self._useFaceMaskVar.set(False)
        self._update_face_preview()
        self._update_merged_preview()
        if self._face_modifier:
            self._face_modifier.update_visuals()

    def getFrame(self) -> tk.Frame:
        return self._faceMaskPanel

    def loadFace(self, config: ImageConfiguration, image) -> None:
        self._config = config
        self._raw_face = image

        self._useFaceMaskVar.set(self._config.faceMask is not None and self._config.faceMask.use_mask)

        self._update_face_preview()
        if self._face_modifier:
            # zoomed in view already open -> update
            self._face_modifier.load_mask(self._raw_face, self._config, self._on_face_mask_changed)

    def _update_face_preview(self):
        # shows mask even if flag is turned off
        masked_image = apply_face_mask_mods(self._raw_face, self._config, True)
        self._resizedImage, self._resizedPhotoImage = loadImageToCanvas(masked_image, self._faceMaskCanvas,
                                                                        resample=PIL.Image.Resampling.NEAREST)

