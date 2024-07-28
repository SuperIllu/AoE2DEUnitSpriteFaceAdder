import tkinter as tk
import tkinter.ttk

from functions.Functions import loadImageToCanvas
from imageInspector import linkImageInspector


class PreviewPanelUI:
    PreviewWidth = 100
    PreviewHeight = 100


    def __init__(self, imagePreviewPanel, parentFrame, autoGenerateMaskVar):
        self._parentFrame = parentFrame
        self._imagePreviewPanel = imagePreviewPanel
        self._autoGenerateOverlayMaskVar = autoGenerateMaskVar
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
        linkImageInspector(self._baseImageCanvas, image, "Base image")
        return loadImageToCanvas(image, self._baseImageCanvas)

    def loadBaseMask(self, image):
        linkImageInspector(self._baseMaskCanvas, image, "Base mask")
        return loadImageToCanvas(image, self._baseMaskCanvas)

    def loadBaseResult(self, image):
        linkImageInspector(self._baseResultCanvas, image, "Base result")
        return loadImageToCanvas(image, self._baseResultCanvas)

    def loadMergedImage(self, image):
        linkImageInspector(self._overlayImageCanvas, image, "Merged result")
        return loadImageToCanvas(image, self._overlayImageCanvas)

    def loadMergedMask(self, image):
        return loadImageToCanvas(image, self._overlayMaskCanvas)

    def loadMergedResult(self, image):
        return loadImageToCanvas(image, self._overlayResultCanvas)
