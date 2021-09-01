import tkinter as tk
from typing import Optional

from managers.imageConfigManager import ImageConfigurationManager, ImageConfiguration
from managers.overlayImageManager import OverlayImageManager
from modificationTab.fileInfoPanel import FileInfoPanel
from modificationTab.fileListPanel import FileListPanel
from modificationTab.globalExporting.globalExportPanel import GlobalExportPanel
from modificationTab.previewPanel.imagePreviewPanel import ImagePreviewPanel
from modificationTab.localExportPanel import LocalExportPanel
from modificationTab.modificationOverlayImageSelection import ModificationOverlaySelectionPanel
from modificationTab.overlayPositionControls import OverlayPositionControls


class ModificationElement:

    def __init__(self, aoeGUI, parentFrame: tk.Frame):
        self._aoeGUI = aoeGUI
        self._parentFrame = parentFrame
        self._imageFileManager = None
        self._imageConfigManager: Optional[ImageConfigurationManager] = None
        self._imageConfiguration: Optional[ImageConfiguration] = ImageConfiguration(None)
        self._overlayImageManager: Optional[OverlayImageManager] = None
        self._buildUI()

        self._selectedFile = None

    @property
    def masterGUI(self):
        return self._aoeGUI

    @property
    def ImageFileManager(self):
        return self._imageFileManager

    @property
    def ImageConfigManager(self):
        return self._imageConfigManager

    @property
    def OverlayImageManager(self):
        return self._overlayImageManager

    def _buildUI(self):
        self._imageList = FileListPanel(self, self._aoeGUI, self._parentFrame)
        self._overlayPanel = tk.Frame(self._parentFrame)

        self._parentFrame.grid_columnconfigure(0, weight=2)
        self._parentFrame.grid_columnconfigure(1, weight=3)
        self._parentFrame.rowconfigure(0, weight=1)
        self._imageList.getFrame().grid(row=0, column=0, sticky="news", padx=(2, 2))
        self._overlayPanel.grid(row=0, column=1, sticky="news", padx=(2, 2))

        self._overlayPanel.grid_columnconfigure(0, weight=1)

        self._overlayPanel.bind('<Return>', lambda event: print("Enter"))

        self._buildFileInfoPanel()
        self._buildPreviewPanel()
        self._buildOverlayPanel()
        self._buildControlPanel()
        self._buildGlobalExportPanel()

    def _buildControlPanel(self):
        self._controlPanel = tk.Frame(self._overlayPanel)
        self._controlPanel.grid_rowconfigure(0, weight=1)
        self._controlPanel.grid_columnconfigure(0, weight=0)
        self._controlPanel.grid_columnconfigure(1, weight=1)
        self._controlPanel.grid(row=3, column=0, columnspan=3, sticky="news")

        self._maskPositionPanel = OverlayPositionControls(self._controlPanel, self._previewPanel, self._aoeGUI)
        self._maskPositionPanel.getFrame().grid(row=0, column=0, sticky="news")
        self._localExportPanel = LocalExportPanel(self._controlPanel, self, self._previewPanel)
        self._localExportPanel.getFrame().grid(row=0, column=1, sticky="news")

    def _buildGlobalExportPanel(self):
        self._globalExportPanel = GlobalExportPanel(self, self._overlayPanel)
        self._globalExportPanel.getFrame().grid(row=4, column=0, sticky="news")

    def _buildFileInfoPanel(self):
        self._fileInfoPanel = FileInfoPanel(self._overlayPanel)
        self._fileInfoPanel.getFrame().grid(row=0, column=0, sticky="news")

    def _buildOverlayPanel(self):
        self._overlayImageSelectionPanel = ModificationOverlaySelectionPanel(self, self._overlayPanel, self._previewPanel)
        self._overlayImageSelectionPanel.getFrame().grid(row=1, column=0, sticky="news")

    def _buildPreviewPanel(self):
        self._previewPanel = ImagePreviewPanel(self, self._overlayPanel)
        self._previewPanel.getFrame().grid(row=2, column=0, sticky="news")

    def getSelectedOverlayImage(self) -> tuple[str, str]:
        return self._overlayImageSelectionPanel.getSelectedOverlayImage()

    def loadConfiguration(self, imageFileManager, overlayImageManager, imageFolderPath: str, maskFolderPath: str):
        """ load the image folders, not when an image in the list is selected """
        self._imageFileManager = imageFileManager
        self._overlayImageManager = overlayImageManager
        self._imageConfigManager = ImageConfigurationManager(self._imageFileManager, overlayImageManager)

        self._imageFolderPath = imageFolderPath
        self._maskFolderPath = maskFolderPath

        self._overlayImageSelectionPanel.loadAvailableOverlayImages(overlayImageManager)
        self._imageList.loadImageList(imageFolderPath)

    def getOutputFolderPath(self):
        return self._aoeGUI.outputFolderPathVar.get()

    def getSelectedFile(self):
        return self._selectedFile

    def selectImageToModify(self, fileName, fullImagePath):
        """ called from the list when selecting an image """
        self._selectedFile = (fileName, fullImagePath)
        self._imageConfiguration = self._imageConfigManager.getConfiguration(self._selectedFile[0],
                                                                             self._imageConfiguration)
        print(f"{fileName} > {self._imageConfiguration}")
        _, fullMaskPath = self._imageFileManager.getMaskToImage(fileName)
        self._fileInfoPanel.loadFilePaths(fullImagePath, fullMaskPath)
        self._previewPanel.loadImageToPreview(self._imageConfiguration)
        self._overlayImageSelectionPanel.loadConfiguration(self._imageConfiguration)
        self._maskPositionPanel.loadConfiguration(self._imageConfiguration)

    def getCurrentImageConfig(self):
        return self._imageConfiguration

    def serialiseState(self):
        return self._imageConfigManager.serialiseState()

    def deserialise(self, serialisedState):
        self._imageConfigManager.deserialiseState(serialisedState)




