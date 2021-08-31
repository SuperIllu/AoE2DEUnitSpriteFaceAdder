from PIL import Image
import tkinter as tk

from functions.Functions import loadImageToCanvas
from functions.imageMerger import mergeImages, createResultImage, generateDeltaMask
from managers.imageConfigManager import ImageConfiguration
from imageInspector import linkImageInspector
from functions.tooltips import BindTooltip
from modificationTab.previewPanel.previewPanelUI import PreviewPanelUI


class ImagePreviewPanel:
    PreviewWidth = 100
    PreviewHeight = 100

    def __init__(self, modificationPanel, parentFrame):
        self._modificationPanel = modificationPanel
        self._parentFrame = parentFrame
        self._buildUI()
        self._baseImage: Image = None
        self._overlayImage: Image = None
        self._overlayOffset = None
        self._overlayImageName = None
        self._mergedImage = None
        self._mergedMask = None
        self._overlayOffset = (0, 0)
        self._imageConfiguration: ImageConfiguration = None

    def _buildUI(self):
        self._autoGenerateOverlayMaskVar = tk.BooleanVar()
        self._autoGenerateOverlayMaskVar.set(True)
        self._previewPanelFrame = PreviewPanelUI(self, self._parentFrame, self._autoGenerateOverlayMaskVar)

    def getFrame(self):
        return self._previewPanelFrame.getFrame()

    def updateAutoGenerateFlag(self, generate: bool):
        if self._imageConfiguration:
            self._imageConfiguration.autoGenerateMask = generate
            self._updateMergedImage()

    def _updateAutoGenerateFlag(self):
        if self._imageConfiguration:
            self._imageConfiguration.autoGenerateMask = self._autoGenerateOverlayMaskVar.get()
            self._updateMergedImage()

    def loadImage(self, configuration: ImageConfiguration):
        """ Called (indirectly) from the list element """
        self._imageConfiguration = configuration
        self._autoGenerateOverlayMaskVar.set(configuration.autoGenerateMask)
        self._baseImage, self._baseMask = \
            self._modificationPanel.ImageConfigManager.getImageAndMask(configuration.imageName)

        self._scaledBaseImage, self._scaledBasePhotoimage = \
            self._previewPanelFrame.loadBaseImage(self._baseImage)

        if self._baseMask:
            self._scaledBaseMaskImage, self._scaledBaseMaskPhotoimage = \
                self._previewPanelFrame.loadBaseMask(self._baseMask)

            resultImage = createResultImage(self._baseImage, self._baseMask)
            self._scaledBaseResultImage, self._scaledBaseResultPhotoimage = \
                self._previewPanelFrame.loadBaseResult(resultImage)

        self._updateMergedImage()

    def _updateMergedImage(self):
        """ creates new images when any overlay information is changed """
        if self._baseImage and self._overlayImage and self._overlayOffset:

            self._mergedImage = mergeImages(self._baseImage, self._overlayImage, self._overlayOffset)
            # these are only temporary, need references to avoid GC
            self._scaledMergedImage, self._scaledMergedPhotoimage = \
                self._previewPanelFrame.loadMergedImage(self._mergedImage)

            if self._autoGenerateOverlayMaskVar.get():
                self._mergedMask = generateDeltaMask(self._baseImage, self._mergedImage, self._baseMask)
            else:
                self._mergedMask = self._baseMask

            # these are only temporary, need references to avoid GC
            self._scaledMergedMask, self._scaledMergedMaskPhotoimage = \
                self._previewPanelFrame.loadMergedMask(self._mergedMask)

            resultImage = createResultImage(self._mergedImage, self._mergedMask)
            # these are only temporary, need references to avoid GC
            self._mergedResultImage, self._mergedResultPhotoimage = \
                self._previewPanelFrame.loadMergedResult(resultImage)

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
        directionMap = {"up": (0, -1), "down": (0, 1), "right": (1, 0), "left": (-1, 0)}
        directionVector = directionMap.get(direction, None)
        if directionVector:
            self._overlayOffset = (self._overlayOffset[0] + directionVector[0],
                                   self._overlayOffset[1] + directionVector[1])
            self._updateMergedImage()
            return self._overlayOffset
        return None