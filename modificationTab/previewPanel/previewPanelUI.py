import tkinter as tk
import tkinter.ttk

from functions.Functions import loadImageToCanvas
from imageInspector import link_image_inspector, ImageInspector


class PreviewPanelUI:
    PreviewWidth = 100
    PreviewHeight = 100

    def __init__(self, imagePreviewPanel, parentFrame, autoGenerateMaskVar):
        self._parentFrame = parentFrame
        self._imagePreviewPanel = imagePreviewPanel
        self._autoGenerateOverlayMaskVar = autoGenerateMaskVar
        self._inspectors: dict = {}
        self._buildUI()

    def _buildUI(self):
        self._previewPanelFrame = tk.LabelFrame(self._parentFrame, text="Preview")
        self._previewPanelFrame.grid_columnconfigure(0, weight=1)
        self._previewPanelFrame.grid_columnconfigure(1, weight=1)
        self._previewPanelFrame.grid_columnconfigure(2, weight=1)
        self._previewPanelFrame.grid_columnconfigure(3, weight=0)  # vertical line
        self._previewPanelFrame.grid_columnconfigure(4, weight=1)  # reserved for face mod panel

        baseImageLabel = tk.Label(self._previewPanelFrame, text="Base Image")
        baseMaskLabel = tk.Label(self._previewPanelFrame, text="Base Mask")
        baseResultLabel = tk.Label(self._previewPanelFrame, text="Base Result")
        self._baseImageCanvas = tk.Canvas(self._previewPanelFrame, bg="white",
                                          width=PreviewPanelUI.PreviewWidth,
                                          height=PreviewPanelUI.PreviewHeight)
        self._baseMaskCanvas = tk.Canvas(self._previewPanelFrame, bg="white",
                                         width=PreviewPanelUI.PreviewWidth,
                                         height=PreviewPanelUI.PreviewHeight)
        self._baseResultCanvas = tk.Canvas(self._previewPanelFrame, bg="white",
                                           width=PreviewPanelUI.PreviewWidth,
                                           height=PreviewPanelUI.PreviewHeight)

        overlayImageLabel = tk.Label(self._previewPanelFrame, text="Overlaid image")
        overlayMaskLabel = tk.Label(self._previewPanelFrame, text="Overlaid mask")
        overlayResultLabel = tk.Label(self._previewPanelFrame, text="Overlaid result")
        self._overlayImageCanvas = tk.Canvas(self._previewPanelFrame, bg="white",
                                             width=PreviewPanelUI.PreviewWidth,
                                             height=PreviewPanelUI.PreviewHeight)
        self._overlayMaskCanvas = tk.Canvas(self._previewPanelFrame, bg="white",
                                            width=PreviewPanelUI.PreviewWidth,
                                            height=PreviewPanelUI.PreviewHeight)
        self._overlayResultCanvas = tk.Canvas(self._previewPanelFrame, bg="white",
                                              width=PreviewPanelUI.PreviewWidth,
                                              height=PreviewPanelUI.PreviewHeight)
        autoGenerateOverlayMaskCheckbox = tk.Checkbutton(self._previewPanelFrame, text="Auto generate overlay mask",
                                                         variable=self._autoGenerateOverlayMaskVar,
                                                         command=self._updateAutoGenerateFlag)

        baseImageLabel.grid(row=0, column=0)
        baseMaskLabel.grid(row=0, column=1)
        baseResultLabel.grid(row=0, column=2)
        self._baseImageCanvas.grid(row=1, column=0)
        self._baseMaskCanvas.grid(row=1, column=1)
        self._baseResultCanvas.grid(row=1, column=2)

        overlayImageLabel.grid(row=2, column=0)
        overlayMaskLabel.grid(row=2, column=1)
        overlayResultLabel.grid(row=2, column=2)
        self._overlayImageCanvas.grid(row=3, column=0)
        self._overlayMaskCanvas.grid(row=3, column=1)
        self._overlayResultCanvas.grid(row=3, column=2)

        autoGenerateOverlayMaskCheckbox.grid(row=4, column=0, columnspan=3)

        # draw vertical line
        (tkinter.ttk.Separator(self._previewPanelFrame, orient=tkinter.VERTICAL).
         grid(column=3, row=0, rowspan=4, sticky="ns"))


    def getFrame(self) -> tk.LabelFrame:
        return self._previewPanelFrame

    def _updateAutoGenerateFlag(self):
        self._imagePreviewPanel.updateAutoGenerateFlag(self._autoGenerateOverlayMaskVar.get())

    def loadBaseImage(self, image):
        self._link_or_update_inspector(image, self._baseImageCanvas,
                                       "Base Image", "_base_img_")
        return loadImageToCanvas(image, self._baseImageCanvas)

    def loadBaseMask(self, image):
        self._link_or_update_inspector(image, self._baseMaskCanvas,
                                       "Base mask", "_base_mask_")
        return loadImageToCanvas(image, self._baseMaskCanvas)

    def loadBaseResult(self, image):
        self._link_or_update_inspector(image, self._baseResultCanvas,
                                       "Base result", "_base_result_")
        return loadImageToCanvas(image, self._baseResultCanvas)

    def loadMergedImage(self, image):
        self._link_or_update_inspector(image, self._overlayImageCanvas,
                                       "Merged Image", "_merged_img_")
        return loadImageToCanvas(image, self._overlayImageCanvas)

    def loadMergedMask(self, image):
        self._link_or_update_inspector(image, self._overlayMaskCanvas,
                                       "Merged mask", "_merged_mask_")
        return loadImageToCanvas(image, self._overlayMaskCanvas)

    def loadMergedResult(self, image):
        self._link_or_update_inspector(image, self._overlayResultCanvas,
                                       "Merged result", "_merged_result_")
        return loadImageToCanvas(image, self._overlayResultCanvas)

    def _link_or_update_inspector(self, image, canvas, image_name, tag):
        inspector: ImageInspector = self._inspectors.get(tag, None)
        if inspector:
            # update already open inspector
            inspector.load_image(image)
        else:
            # no inspector open -> open a new instance
            self._link_inspector(image, canvas, image_name, tag)

    def _link_inspector(self, image, canvas, image_name: str, tag: str):
        def _remember_inspector(inspector, tag_: str):
            self._inspectors[tag_] = inspector

        def _forget_inspector(tag_: str):
            del self._inspectors[tag_]

        def _can_open_inspector(tag_: str):
            return self._inspectors.get(tag_, None) is None

        link_image_inspector(canvas, image, image_name,
                             lambda insp: _remember_inspector(insp, tag),
                             lambda: _forget_inspector(tag),
                             lambda: _can_open_inspector(tag)
                             )
