from PIL import Image
import tkinter as tk

from Functions import loadImageToCanvas
from imageMerger import mergeImages, createResultImage, generateDeltaMask
from imageConfigManager import ImageConfiguration
from imageInspector import linkImageInspector


class ImagePreviewPanel:
    PreviewWidth = 100
    PreviewHeight = 100

    def __init__(self, modificationPanel, parentFrame):
        self._modificationPanel = modificationPanel
        self._parentFrame = parentFrame
        self._buildUI()
        self._baseImage = None
        self._overlayImage = None
        self._overlayOffset = None
        self._overlayImageName = None
        self._mergedImage = None
        self._mergedMask = None
        self._overlayOffset = (0, 0)
        self._imageConfiguration: ImageConfiguration = None

    def _buildUI(self):
        self._previewPanel = tk.LabelFrame(self._parentFrame, text="Preview")
        self._previewPanel.grid_columnconfigure(0, weight=1)
        self._previewPanel.grid_columnconfigure(1, weight=1)
        self._previewPanel.grid_columnconfigure(2, weight=1)

        baseImageLabel = tk.Label(self._previewPanel, text="Base Image")
        baseMaskLabel = tk.Label(self._previewPanel, text="Base Mask")
        baseResultLabel = tk.Label(self._previewPanel, text="Base Result")
        self._baseImageCanvas = tk.Canvas(self._previewPanel, bg="white",
                                          width=ImagePreviewPanel.PreviewWidth,
                                          height=ImagePreviewPanel.PreviewHeight)
        self._baseMaskCanvas = tk.Canvas(self._previewPanel, bg="white",
                                         width=ImagePreviewPanel.PreviewWidth,
                                         height=ImagePreviewPanel.PreviewHeight)
        self._baseResultCanvas = tk.Canvas(self._previewPanel, bg="white",
                                           width=ImagePreviewPanel.PreviewWidth,
                                           height=ImagePreviewPanel.PreviewHeight)

        overlayImageLabel = tk.Label(self._previewPanel, text="Overlaid image")
        overlayMaskLabel = tk.Label(self._previewPanel, text="Overlaid mask")
        overlayResultLabel = tk.Label(self._previewPanel, text="Overlaid result")
        self._overlayImageCanvas = tk.Canvas(self._previewPanel, bg="white",
                                             width=ImagePreviewPanel.PreviewWidth,
                                             height=ImagePreviewPanel.PreviewHeight)
        self._overlayMaskCanvas = tk.Canvas(self._previewPanel, bg="white",
                                            width=ImagePreviewPanel.PreviewWidth,
                                            height=ImagePreviewPanel.PreviewHeight)
        self._overlayResultCanvas = tk.Canvas(self._previewPanel, bg="white",
                                              width=ImagePreviewPanel.PreviewWidth,
                                              height=ImagePreviewPanel.PreviewHeight)
        self._autoGenerateOverlayMaskVar = tk.BooleanVar()
        self._autoGenerateOverlayMaskVar.set(True)
        autoGenerateOverlayMaskCheckbox = tk.Checkbutton(self._previewPanel, text="Auto generate overlay mask",
                                                         variable=self._autoGenerateOverlayMaskVar)

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

    def getFrame(self):
        return self._previewPanel

    def loadImage(self, configuration: ImageConfiguration):
        """ Called (indirectly) from the list element """
        self._imageConfiguration = configuration
        self._baseImage, self._baseMask = \
            self._modificationPanel.ImageConfigManager.getImageAndMask(configuration.image)

        self._scaledBaseImage, self._scaledBasePhotoimage = \
            loadImageToCanvas(self._baseImage, self._baseImageCanvas)

        if self._baseMask:
            self._scaledBaseMaskImage, self._scaledBaseMaskPhotoimage = \
                loadImageToCanvas(self._baseMask, self._baseMaskCanvas)
            linkImageInspector(self._baseMaskCanvas, self._baseMask)

            resultImage = createResultImage(self._baseImage, self._baseMask)
            self._scaledBaseResultImage, self._scaledBaseResultPhotoimage = \
                loadImageToCanvas(resultImage, self._baseResultCanvas)
            linkImageInspector(self._baseResultCanvas, self._scaledBaseResultImage)

        linkImageInspector(self._baseImageCanvas, self._baseImage)

        self._updateMergedImage()

    def _updateMergedImage(self):
        if self._baseImage and self._overlayImage and self._overlayOffset:

            self._mergedImage = mergeImages(self._baseImage, self._overlayImage, self._overlayOffset)
            # these are only temporary, need refernces to avoid GC
            self._scaledMergedImage, self._scaledMergedPhotoimage = \
                loadImageToCanvas(self._mergedImage, self._overlayImageCanvas)

            if self._autoGenerateOverlayMaskVar.get():
                self._mergedMask = generateDeltaMask(self._baseImage, self._mergedImage, self._baseMask)
            else:
                self._mergedMask = self._baseMask

            # these are only temporary, need refernces to avoid GC
            self._scaledMergedMask, self._scaledMergedMaskPhotoimage = \
                loadImageToCanvas(self._mergedMask, self._overlayMaskCanvas)

            resultImage = createResultImage(self._mergedImage, self._mergedMask)
            # these are only temporary, need refernces to avoid GC
            self._mergedResultImage, self._mergedResultPhotoimage = \
                loadImageToCanvas(resultImage, self._overlayResultCanvas)

    def getMergedImage(self):
        return self._mergedImage

    def getMergedMask(self):
        return self._mergedMask

    def setOverlayImage(self, overlayImageName: str, fullOverlayImageFilePath: Image):
        if self._overlayImageName != overlayImageName:
            self._overlayImage = Image.open(fullOverlayImageFilePath)
            self._updateMergedImage()
        self._overlayImageName = overlayImageName
        self._updateImageConfiguration()

    def getOverlayOffset(self):
        return self._overlayOffset

    def _updateImageConfiguration(self):
        if self._imageConfiguration:
            self._imageConfiguration.overlayImage = self._overlayImage
            self._imageConfiguration.offset = self._overlayOffset

    def setOverlayPosition(self, position: tuple[int, int]) -> tuple[int, int]:
        if position != self._overlayOffset:
            self._overlayOffset = position
            self._updateMergedImage()
        self._updateImageConfiguration()
        return self._overlayOffset

    def moveOverlay(self, direction) -> tuple[int, int]:
        direction = direction.lower()
        directionMap = {"up": (0, -1), "down": (0, 1), "right":(1, 0), "left": (-1, 0)}
        directionVector = directionMap.get(direction, None)
        if directionVector:
            self._overlayOffset = (self._overlayOffset[0] + directionVector[0],
                                   self._overlayOffset[1] + directionVector[1])
            self._updateMergedImage()
            return self._overlayOffset
        return None
