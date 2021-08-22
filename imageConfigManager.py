from PIL import Image
from imageMerger import mergeImages, generateDeltaMask
from imageFileManager import ImageFileManager


class ImageConfiguration:

    def __init__(self, image, overlayImage: str = None, offset: tuple[int, int] = None):
        self._image = image
        self._overlayImage = overlayImage
        self._offset = offset

    def __repr__(self):
        return f"{self._image}-{self._offset}-{self._overlayImage}"

    @property
    def image(self):
        return self._image

    @property
    def overlayImage(self):
        return self._overlayImage

    @overlayImage.setter
    def overlayImage(self, overlayImage):
        self._overlayImage = overlayImage

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset


class ImageConfigurationManager:

    def __init__(self, fileManager: ImageFileManager):
        self._configurationMap = {}
        self._fileManager = fileManager

    def getAllConfiguredImages(self) -> list[str]:
        return list(self._configurationMap.keys())

    def hasConfiguration(self, imageName: str) -> bool:
        return imageName in self._configurationMap.keys()

    def getConfiguration(self, imageName:str) -> ImageConfiguration:
        if imageName not in self._configurationMap.keys():
            self._configurationMap[imageName] = ImageConfiguration(imageName)
        return self._configurationMap.get(imageName, None)

    def getImageAndMask(self, imageName: str) -> tuple[Image, Image]:
        """ Returns new, unmodified images """
        fullImagePath = self._fileManager.getFullImagePath(imageName)
        maskName, maskPath = self._fileManager.getMaskToImage(imageName)
        return Image.open(fullImagePath), Image.open(maskPath)

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
