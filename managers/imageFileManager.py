import os


class ImageFileManager:

    @staticmethod
    def getMaskName(imageName) -> str:
        """ Input: just the name, not the entire path"""
        imageNameParts = os.path.splitext(imageName)
        if len(imageNameParts) != 2:
            raise Exception(f"image name could not be dissected: {imageName}")
        return f"{imageNameParts[0]}d{imageNameParts[1]}"

    @staticmethod
    def getImageName(maskName) -> str:
        maskNameParts = os.path.splitext(maskName)
        if len(maskNameParts) != 2:
            raise Exception(f"image name could not be dissected: {maskName}")
        return f"{maskNameParts[0][:-1]}{maskNameParts[1]}"

    @staticmethod
    def evaluateCheckResult(result):
        return len(result[0]) == len(result[1]) == 0 and result[2]

    def __init__(self, imageFileFolder: str, maskFileFolder: str, overlayManager):
        self._imageFileFolder = imageFileFolder
        self._maskFileFolder = maskFileFolder
        self._imageMap = {}
        self._maskMap = {}
        self._overlayManager = overlayManager

        self.load()

    def load(self) -> bool:
        """ creates the internal maps for images->filepath and mask->filepath """
        if not os.path.exists(self._imageFileFolder) or not os.path.exists(self._maskFileFolder):
            return False
        imageFiles = os.listdir(self._imageFileFolder)
        for file in imageFiles:
            fullPath = f"{self._imageFileFolder}{os.path.sep}{file}"
            if not os.path.isfile(fullPath):
                continue
            if not file.lower().endswith(".bmp"):
                continue
            if file.lower().endswith("d.bmp"):
                continue
            self._imageMap[file] = fullPath

        maskFiles = os.listdir(self._maskFileFolder)
        for file in maskFiles:
            fullPath = f"{self._maskFileFolder}{os.path.sep}{file}"
            if not os.path.isfile(fullPath):
                continue
            if not file.lower().endswith("d.bmp"):
                continue
            self._maskMap[file] = fullPath
        return True

    def checkFileToMapConsitency(self) -> tuple[list, list, bool]:
        """ returns a tuple of lists:
         list0: any images for which no masks could be found
         list1: any masks for which no images could be found"""
        imagesWithMissingMasks = []
        masksWithMissingImages = []
        for image in self._imageMap.keys():
            expectedMaskName = ImageFileManager.getMaskName(image)
            if expectedMaskName not in self._maskMap.keys():
                imagesWithMissingMasks.append(image)
        for mask in self._maskMap.keys():
            expectedImageName = ImageFileManager.getImageName(mask)
            if expectedImageName not in self._imageMap.keys():
                masksWithMissingImages.append(mask)

        return (imagesWithMissingMasks, masksWithMissingImages, len(self._overlayManager.getOverlayImages()) > 0)

    def getMaskToImage(self, fullImagePath) -> tuple[str, str]:
        """ returns the file name and full path of the of corresponding mask """
        maskName = ImageFileManager.getMaskName(fullImagePath)
        return (maskName, self._maskMap.get(maskName, None))

    def getFullImagePath(self, imageName) -> str:
        return self._imageMap.get(imageName, None)

    def getAllImageNames(self) -> list[str]:
        return list(self._imageMap.keys())

    def getAllMaskNames(self) -> list[str]:
        return list(self._maskMap.keys())

