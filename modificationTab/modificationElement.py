import os
import tkinter as tk
from typing import Optional

from managers.imageConfigManager import ImageConfigurationManager, ImageConfiguration
from modificationTab.fileInfoPanel import FileInfoPanel
from modificationTab.fileListPanel import FileListPanel
from modificationTab.globalExporting.globalExportPanel import GlobalExportPanel
from modificationTab.imagePreviewPanel import ImagePreviewPanel
from modificationTab.localExportPanel import LocalExportPanel
from modificationTab.overlayImageSelection import OverlaySelectionPanel
from modificationTab.overlayPositionControls import OverlayPositionControls


class ModificationElement:

    def __init__(self, aoeGUI, parentFrame: tk.Frame):
        self._aoeGUI = aoeGUI
        self._parentFrame = parentFrame
        self._imageFileManager = None
        self._imageConfigManager: Optional[ImageConfigurationManager] = None
        self._imageConfiguration: Optional[ImageConfiguration] = None
        self._buildUI()

        self._selectedFile = None

    @property
    def masterGUI(self):
        return self._aoeGUI

    @property
    def ImageFileManager(self):
        return self._imageFileManager

    @ImageFileManager.setter
    def ImageFileManager(self, ifm):
        self._imageFileManager = ifm
        self._imageConfigManager = ImageConfigurationManager(ifm)

    @property
    def ImageConfigManager(self):
        return self._imageConfigManager

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
        self._overlayImageSelectionPanel = OverlaySelectionPanel(self._overlayPanel, self._previewPanel)
        self._overlayImageSelectionPanel.getFrame().grid(row=1, column=0, sticky="news")

    def _buildPreviewPanel(self):
        self._previewPanel = ImagePreviewPanel(self, self._overlayPanel)
        self._previewPanel.getFrame().grid(row=2, column=0, sticky="news")

    def getSelectedOverlayImage(self) -> tuple[str, str]:
        return self._overlayImageSelectionPanel.getSelectedOverlayImage()

    def loadConfiguration(self, imageFolderPath: str, maskFolderPath: str, overlayImages:dict):
        self._imageFolderPath = imageFolderPath
        self._maskFolderPath = maskFolderPath

        self._overlayImageSelectionPanel.loadAvailableOverlayImages(overlayImages)
        self._imageList.loadImageList(imageFolderPath)

    def getOutputFolderPath(self):
        return self._aoeGUI.outputFolderPathVar.get()

    def getSelectedFile(self):
        return self._selectedFile

    def loadImage(self, fileName, fullImagePath):
        """ called from the list when selecting an image """
        self._selectedFile = (fileName, fullImagePath)
        self._imageConfiguration = self._imageConfigManager.getConfiguration(self._selectedFile[0],
                                                                             self._imageConfiguration)
        _, fullMaskPath = self._imageFileManager.getMaskToImage(fileName)
        self._fileInfoPanel.loadFilePaths(fullImagePath, fullMaskPath)
        self._previewPanel.loadImage(self._imageConfiguration)
        self._maskPositionPanel.loadConfiguration(self._imageConfiguration)

    def serialiseState(self):
        return self._imageConfigManager.serialiseState()

    def deserialise(self, serialisedState):
        self._imageConfigManager.deserialiseState(serialisedState)




