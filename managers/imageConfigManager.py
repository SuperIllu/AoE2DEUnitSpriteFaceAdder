import dataclasses
from typing import Optional
from dataclasses import dataclass

from PIL import Image
from functions.imageMerger import mergeImages, generateDeltaMask
from managers.imageFileManager import ImageFileManager
from managers.overlayImageManager import OverlayImageManager


@dataclass(order=True)
class ImageConfiguration:
    imageName: Image
    hasOverlay: bool = True
    overlayImageIndex: int = 0
    offset: tuple[int, int] = (0, 0)
    autoGenerateMask: bool = True

    def serialise(self):
        return dataclasses.asdict(self)


class ImageConfigurationManager:

    def __init__(self, fileManager: ImageFileManager, overlayImageManager: OverlayImageManager):
        self._configurationMap = {}
        self._fileManager = fileManager
        self._overlayManager = overlayImageManager

    def getAllConfiguredImages(self) -> list[str]:
        return list(self._configurationMap.keys())

    def hasConfiguration(self, imageName: str) -> bool:
        return imageName in self._configurationMap.keys()

    def getConfiguration(self, imageName:str, configBlueprint: Optional[ImageConfiguration]=None) -> ImageConfiguration:
        if imageName not in self._configurationMap.keys():
            if configBlueprint:
                imageConfig = dataclasses.replace(configBlueprint, imageName=imageName)
            else:
                imageConfig = ImageConfiguration(imageName)
            self._configurationMap[imageName] = imageConfig
        return self._configurationMap.get(imageName, None)

    def getImageAndMask(self, imageName: str) -> tuple[Image, Image]:
        """ Returns new, unmodified images """
        fullImagePath = self._fileManager.getFullImagePath(imageName)
        maskName, maskPath = self._fileManager.getMaskToImage(imageName)
        maskImage = Image.open(maskPath) if maskPath else None
        return Image.open(fullImagePath), maskImage

    def generateImagesToExport(self, imageName: str) -> tuple[Image, Image]:
        """ Generates both image and mask to be exported """

        imageImage, maskImage = self.getImageAndMask(imageName)

        if not self.hasConfiguration(imageName):
            print(f"[WARN] {imageName} has no configuration. Returns base (image, mask)")
            return (imageImage, maskImage)

        configuration = self.getConfiguration(imageName)
        overlayImagePath = self._overlayManager.getImageForIndex(configuration.overlayImageIndex)
        overlayImage = Image.open(overlayImagePath)
        overlayImageOffset = configuration.offset

        if not (overlayImage and overlayImageOffset):
            # return unmodified images
            return (imageImage, maskImage)

        mergedImage: Image = mergeImages(imageImage, overlayImage, overlayImageOffset)
        if configuration.autoGenerateMask:
            mergedMask: Image = generateDeltaMask(imageImage, mergedImage, maskImage)
        else:
            mergedMask:Image = maskImage
        return (mergedImage, mergedMask)

    def serialiseState(self):
        return [config.serialise() for config in self._configurationMap.values()]
