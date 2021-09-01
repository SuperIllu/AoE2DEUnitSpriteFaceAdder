from PIL import Image
import tkinter as tk

from functions.imageMerger import mergeImages, createResultImage, generateDeltaMask
from managers.imageConfigManager import ImageConfiguration
from modificationTab.previewPanel.previewPanelUI import PreviewPanelUI


class ImagePreviewPanel:
    PreviewWidth = 100
    PreviewHeight = 100

    def __init__(self, modificationPanel, parentFrame):
        self._modificationPanel = modificationPanel
        self._parentFrame = parentFrame
        self._buildUI()
        self._baseImage: Image = None
        self._overlayImageIndex: int = -1
        self._overlayOffset = None
        self._mergedImage = None
        self._mergedMask = None
        self._overlayOffset = (0, 0)

    def _buildUI(self):
        self._autoGenerateOverlayMaskVar = tk.BooleanVar()
        self._autoGenerateOverlayMaskVar.set(True)
        self._previewPanelFrame = PreviewPanelUI(self, self._parentFrame, self._autoGenerateOverlayMaskVar)

    def getFrame(self):
        return self._previewPanelFrame.getFrame()

    def updateAutoGenerateFlag(self, generate: bool):
        configuration = self._modificationPanel.getCurrentImageConfig()
        if configuration:
            configuration.autoGenerateMask = generate
            self._updateMergedImage()

    def loadImageToPreview(self, configuration: ImageConfiguration):
        """ Called (indirectly) from the list element """
        self._autoGenerateOverlayMaskVar.set(configuration.autoGenerateMask)
        overlayImagePath = self._modificationPanel.OverlayImageManager.getImageForIndex(configuration.overlayImageIndex)
        self._overlayImage = Image.open(overlayImagePath)

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
        if self._baseImage:
            configuration = self._modificationPanel.getCurrentImageConfig()
            if configuration is None:
                print("No configuration -> skip")
                return

            if configuration.hasOverlay:
                fullOverlayImageFilePath = self._modificationPanel.OverlayImageManager. \
                    getImageForIndex(configuration.overlayImageIndex)
                overlayImage = Image.open(fullOverlayImageFilePath)

                self._mergedImage = mergeImages(self._baseImage, overlayImage, configuration)


                if self._autoGenerateOverlayMaskVar.get():
                    self._mergedMask = generateDeltaMask(self._baseImage, self._mergedImage, self._baseMask)
                else:
                    self._mergedMask = self._baseMask
            else:
                self._mergedImage = self._baseImage
                self._mergedMask = self._baseMask

            # these are only temporary, need references to avoid GC
            self._scaledMergedImage, self._scaledMergedPhotoimage = \
                self._previewPanelFrame.loadMergedImage(self._mergedImage)

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

    def updateFromConfiguration(self):
        self._updateMergedImage()

    def getOverlayOffset(self) -> tuple[int, int]:
        config = self._modificationPanel.getCurrentImageConfig()
        if config is not None:
            return self._modificationPanel.getCurrentImageConfig().offset
        else:
            return (0, 0)

    def setOverlayPosition(self, position: tuple[int, int]) -> tuple[int, int]:
        if position != self._modificationPanel.getCurrentImageConfig().offset:
            self._modificationPanel.getCurrentImageConfig().offset = position
            self._updateMergedImage()
        return position

    def moveOverlay(self, direction) -> tuple[int, int]:
        direction = direction.lower()
        directionMap = {"up": (0, -1), "down": (0, 1), "right": (1, 0), "left": (-1, 0)}
        directionVector = directionMap.get(direction, None)
        currentPosition = self._modificationPanel.getCurrentImageConfig().offset
        if directionVector:
            newPosition = (currentPosition[0] + directionVector[0],
                           currentPosition[1] + directionVector[1])
            self._modificationPanel.getCurrentImageConfig().offset = newPosition
            self._updateMergedImage()
            return newPosition
        return None
