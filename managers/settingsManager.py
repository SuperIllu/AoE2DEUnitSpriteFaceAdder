from typing import Optional


class MaskSettings:

    def __init__(self):
        self.Include = (255, 255, 255)
        self.Exclude = (255, 0, 255)
        self.Shadow = (255, 0, 0)


class SettingsManager:

    def __init__(self):
        self.setDefaultSettings()

    def setDefaultSettings(self):
        self._transparencyThreshold = 250
        self._imageResamplingMethod = None
        self._filterColours = [(255, 0, 255, 255), (255, 0, 0, 255), # pink with alpha
                               (255, 0, 255)] # pink without alpha
        self._maskSettings = MaskSettings()

    @property
    def TransparencyThreshold(self) -> int:
        return self._transparencyThreshold

    @TransparencyThreshold.setter
    def TransparencyThreshold(self, value: int):
        self._transparencyThreshold = value

    @property
    def ResamplingMethod(self) -> Optional[int]:
        return self._imageResamplingMethod

    @ResamplingMethod.setter
    def ResamplingMethod(self, value: Optional[int]):
        self._imageResamplingMethod = value

    @property
    def MaskSetting(self) -> MaskSettings:
        return self._maskSettings

    @MaskSetting.setter
    def MaskSetting(self, value: MaskSettings):
        self._maskSettings = value
