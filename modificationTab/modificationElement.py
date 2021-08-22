import os
import tkinter as tk
from PIL import Image, ImageTk

from Functions import calculatePreviewImageSize, loadImagePathToCanvas, trimStringToElementLength
from imageConfigManager import ImageConfigurationManager
from modificationTab.fileInfoPanel import FileInfoPanel
from modificationTab.fileListPanel import FileListPanel
from modificationTab.globalExportPanel import GlobalExportPanel
from modificationTab.imagePreviewPanel import ImagePreviewPanel
from modificationTab.localExportPanel import LocalExportPanel
from modificationTab.overlayPositionControls import OverlayPositionControls


class ModificationElement:

    def __init__(self, aoeGUI, parentFrame: tk.Frame):
        self._aoeGUI = aoeGUI
        self._parentFrame = parentFrame
        self._imageFileManager = None
        self._imageConfigManager: ImageConfigurationManager = None
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

        self._buildFileInfoPanel()
        self._buildOverlayPanel()
        self._buildPreviewPanel()
        self._buildControlPanel()
        self._buildGlobalExportPanel()

    def _buildControlPanel(self):
        self._controlPanel = tk.Frame(self._overlayPanel)
        self._controlPanel.grid_rowconfigure(0, weight=1)
        self._controlPanel.grid_columnconfigure(0, weight=0)
        self._controlPanel.grid_columnconfigure(1, weight=1)
        self._controlPanel.grid(row=3, column=0, columnspan=3, sticky="news")

        self._maskPositionPanel = OverlayPositionControls(self._controlPanel, self._previewPanel)
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
        overlaySelectionPanel = tk.LabelFrame(self._overlayPanel, text="Overlay Image")
        overlaySelectionPanel.grid_columnconfigure(0, weight=0)
        overlaySelectionPanel.grid_columnconfigure(1, weight=1)
        overlaySelectionPanel.grid_rowconfigure(0, weight=1)
        overlaySelectionPanel.grid(row=1, column=0, sticky="news")

        self._useOverlayVar = tk.BooleanVar()
        self._useOverlayVar.set(True)
        self._selectedOverlayVar = tk.StringVar()
        self._selectedOverlayVar.set("None")
        self._selectedOverlayFilePathVar = tk.StringVar()

        useOverlayCheckbox = tk.Checkbutton(overlaySelectionPanel, text="Use an image", variable=self._useOverlayVar)
        self._overlaySelectionDropdown = tk.OptionMenu(overlaySelectionPanel, self._selectedOverlayVar,
                                                 *[""], command=self._newOverlaySelected)
        self._overlaySelectionDropdown.config(width=1)
        overlayFilePathLabel = tk.Label(overlaySelectionPanel, text="File path:")
        overlayFilePathSelection = tk.Label(overlaySelectionPanel, textvariable=self._selectedOverlayFilePathVar,
                                            width=10, bg="white")

        useOverlayCheckbox.grid(row=0, column=0, sticky="news", padx=(5, 5), pady=(2, 2))
        self._overlaySelectionDropdown.grid(row=0, column=1, padx=(10, 10), pady=(2, 2), sticky="news")
        overlayFilePathLabel.grid(row=1, column=0, sticky="news", padx=(5, 5), pady=(2, 2))
        overlayFilePathSelection.grid(row=1, column=1, sticky="news", padx=(5, 5), pady=(2, 2))

    def _newOverlaySelected(self, overlayFileName):
        if self._useOverlayVar.get():
            self._selectedOverlayVar.set(overlayFileName)
            fullOverlayFilePath = self._overlayImages[overlayFileName]
            self._previewPanel.setOverlayImage(overlayFileName, fullOverlayFilePath)
            self._selectedOverlayFilePathVar.set(trimStringToElementLength(fullOverlayFilePath))

    def _buildPreviewPanel(self):
        self._previewPanel = ImagePreviewPanel(self, self._overlayPanel)
        self._previewPanel.getFrame().grid(row=2, column=0, sticky="news")

    def getSelectedOverlayImage(self) -> tuple[str, str]:
        selectedKey = self._selectedOverlayVar.get()
        return (selectedKey, self._overlayImages[selectedKey])

    def loadConfiguration(self, imageFolderPath: str, maskFolderPath: str, overlayImages:dict):
        self._imageFolderPath = imageFolderPath
        self._maskFolderPath = maskFolderPath
        self._overlayImages = overlayImages

        self._overlaySelectionDropdown.children["menu"].delete(0, tk.END)
        for overlayImage in overlayImages.items():
            self._overlaySelectionDropdown. \
            children["menu"].add_command(label=overlayImage[0],
                                         command=lambda file=overlayImage[0]: self._newOverlaySelected(file))

        if len(overlayImages.keys()) > 0:
            firstOverlayImage = sorted(overlayImages.keys())[0]
            self._newOverlaySelected(firstOverlayImage)
        self._imageList.loadImageList(imageFolderPath)

    def getOutputFolderPath(self):
        return self._aoeGUI.outputFolderPathVar.get()

    def getSelectedFile(self):
        return self._selectedFile

    def loadImage(self, fileName, fullImagePath):
        """ called from the list when selecting an image """
        self._selectedFile = (fileName, fullImagePath)
        self._imageConfiguration = self._imageConfigManager.getConfiguration(self._selectedFile[0])
        _, fullMaskPath = self._imageFileManager.getMaskToImage(fileName)
        self._fileInfoPanel.loadFilePaths(fullImagePath, fullMaskPath)
        self._previewPanel.loadImage(self._imageConfiguration)
        self._maskPositionPanel.loadConfiguration(self._imageConfiguration)






