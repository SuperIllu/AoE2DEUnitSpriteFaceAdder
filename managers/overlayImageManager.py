import os
from typing import Optional


class OverlayImageManager:

    def __init__(self):
        self._overlayImages = []
        self._overlayDisplayNamesMap: dict[str, int] = {}
        self._indexToDisplayNameMap: dict[int, str] = {}

    def addImage(self, fullImagePath: str) -> Optional[tuple[str, int]]:
        if fullImagePath not in self._overlayImages:
            self._overlayImages.append(fullImagePath)
            return self._generateDisplayName(fullImagePath, len(self._overlayImages)-1)
        return None

    def removeImage(self, index: int) -> Optional[dict[str, int]]:
        if len(self._overlayImages) > index >= 0:
            del self._overlayImages[index]
            return self._regenerateDisplayNames()
        return None

    def removeAllImages(self) -> None:
        self._overlayImages.clear()
        self._overlayDisplayNamesMap.clear()

    def _generateDisplayName(self, fullImagePath: str, index: int) -> tuple[str, int]:
        fileName = os.path.basename(fullImagePath)
        displayName = f"{index+1} - {fileName}"
        self._overlayDisplayNamesMap[displayName] = index
        self._indexToDisplayNameMap[index] = displayName
        return (displayName, index)

    def _regenerateDisplayNames(self) -> dict[str, int]:
        self._indexToDisplayNameMap.clear()
        self._overlayDisplayNamesMap.clear()
        for index, fullImagePath in enumerate(self._overlayImages):
            self._generateDisplayName(fullImagePath, index)
        return self._overlayDisplayNamesMap


    def getImageForIndex(self, index: int) -> Optional[str]:
        """ returns the full image path """
        if len(self._overlayImages) > index >= 0:
            return self._overlayImages[index]
        else:
            return None

    def getImageForDisplayName(self, displayName: str) -> str:
        imageIndex = self._overlayDisplayNamesMap.get(displayName, None)
        if imageIndex is not None:
            return self.getImageForIndex(imageIndex)

    def getIndexFromDisplayName(self, displayName: str) -> int:
        return self._overlayDisplayNamesMap.get(displayName)

    def getOverlayDisplayNames(self) -> dict[str, int]:
        return self._overlayDisplayNamesMap.copy()

    def getOverlayImages(self) -> [str]:
        return self._overlayImages.copy()

    def getDisplayNameFromIndex(self, index: int) -> str:
        return self._indexToDisplayNameMap[index]

    def serialiseState(self):
        return {index: filePath for index, filePath in enumerate(self._overlayImages)}
