import dataclasses
from typing import Optional, Any, Type
from dataclasses import dataclass

from PIL import Image

from functions.faceMaskUtils import FaceMaskConfig, apply_face_mask_mods
from functions.imageMerger import mergeImages, generateDeltaMask
from managers.imageFileManager import ImageFileManager
from managers.overlayImageManager import OverlayImageManager


@dataclass(order=True)
class ImageConfiguration:
    imageName: str
    hasOverlay: bool = True
    overlayImageIndex: int = 0
    offset: tuple[int, int] = (0, 0)
    autoGenerateMask: bool = True
    faceMask: FaceMaskConfig = None


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

    def deleteConfiguration(self, imageName):
        if self.hasConfiguration(imageName):
            del self._configurationMap[imageName]

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

        overlayImage = apply_face_mask_mods(overlayImage, configuration)

        mergedImage: Image = mergeImages(imageImage, overlayImage, overlayImageOffset)
        if configuration.autoGenerateMask:
            mergedMask: Image = generateDeltaMask(imageImage, mergedImage, maskImage)
        else:
            mergedMask:Image = maskImage
        return (mergedImage, mergedMask)

    def serialiseState(self):
        return [config.serialise() for config in self._configurationMap.values()]

    def deserialiseState(self, state: list[dict]):
        self._configurationMap.clear()
        if state:
            for configEntry in state:
                self._deserialiseEntry(configEntry)

    def _deserialiseEntry(self, entry: dict):
        # config_entry = ImageConfiguration(**entry)
        config_entry = self._parse_nested_data_classes(ImageConfiguration, entry)
        self._configurationMap[entry['imageName']] = config_entry

    def _parse_nested_data_classes(self, data_class: Type[Any], data: dict):
        """
        Recursively convert a dictionary into a dataclass instance.
        """
        if not hasattr(data_class, '__dataclass_fields__'):
            return data  # If it's not a dataclass, return the data as is

        fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
        kwargs = {}

        for field_name, field_type in fieldtypes.items():
            try:
                # Recursively handle each field
                data_value = data[field_name]
                if data_value is None:
                    kwargs[field_name] = None
                else:
                    kwargs[field_name] = self._parse_nested_data_classes(field_type, data_value)
            except Exception as e:
                # Log the problematic field and its data
                print(f"Error while processing field '{field_name}' with data: {data.get(field_name, 'N/A')}")
                raise e

        return data_class(**kwargs)


