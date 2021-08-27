import dataclasses
from typing import Optional

from PIL import Image
from imageMerger import mergeImages, generateDeltaMask
from imageFileManager import ImageFileManager
from dataclasses import dataclass


@dataclass(order=True)
class ImageConfiguration:
    imageName: Image
    overlayImage: Image = None
    offset: tuple[int, int] = (0, 0)
    autoGenerateShadow: bool = True


class ImageConfigurationManager:

    def __init__(self, fileManager: ImageFileManager):
        self._configurationMap = {}
        self._fileManager = fileManager

    def getAllConfiguredImages(self) -> list[str]:
        return list(self._configurationMap.keys())

    def hasConfiguration(self, imageName: str) -> bool:
        return imageName in self._configurationMap.keys()

    def getConfiguration(self, imageName:str, configBlueprint: Optional[ImageConfiguration]) -> ImageConfiguration:
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
        overlayImage = configuration.overlayImage
        overlayImageOffset = configuration.offset

        if not (overlayImage and overlayImageOffset):
            # return unmodified images
            return (imageImage, maskImage)

        mergedImage: Image = mergeImages(imageImage, overlayImage, overlayImageOffset)
        mergedMask: Image = generateDeltaMask(imageImage, mergedImage, maskImage)
        return (mergedImage, mergedMask)
