import tkinter as tk

from functions.Functions import trimStringToElementLength, loadImagePathToCanvas
from managers.imageConfigManager import ImageConfiguration
from managers.overlayImageManager import OverlayImageManager


class ModificationOverlaySelectionPanel:

    def __init__(self, modificationElement, parentFrame, previewPanel):
        self._modificaitonElement = modificationElement
        self._parentFrame = parentFrame
        self._previewPanel = previewPanel
        self._overlayImageManager: OverlayImageManager
        self._buildUI()

    def _buildUI(self):
        self._overlaySelectionPanel = tk.LabelFrame(self._parentFrame, text="Overlay Image")
        self._overlaySelectionPanel.grid_columnconfigure(0, weight=0)
        self._overlaySelectionPanel.grid_columnconfigure(1, weight=1)
        self._overlaySelectionPanel.grid_rowconfigure(0, weight=1)
        self._overlaySelectionPanel.grid(row=1, column=0, sticky="news")

        self._useOverlayVar = tk.BooleanVar()
        self._useOverlayVar.set(True)
        self._selectedOverlayVar = tk.StringVar()
        self._selectedOverlayVar.set("None")
        self._selectedOverlayFilePathVar = tk.StringVar()

        useOverlayCheckbox = tk.Checkbutton(self._overlaySelectionPanel, text="Use an image",
                                            variable=self._useOverlayVar, command=self._toggleUseOverlayImage)
        self._overlaySelectionDropdown = tk.OptionMenu(self._overlaySelectionPanel, self._selectedOverlayVar,
                                                       *[""], command=self._newOverlaySelected)
        self._overlaySelectionDropdown.config(width=1)
        overlayFilePathLabel = tk.Label(self._overlaySelectionPanel, text="File path:")
        overlayFilePathSelection = tk.Label(self._overlaySelectionPanel, textvariable=self._selectedOverlayFilePathVar,
                                            width=10, bg="white", anchor="e")

        self._selectedOverlayPreview = tk.Canvas(self._overlaySelectionPanel, width=50, height=50, bg="white")

        useOverlayCheckbox.grid(row=0, column=0, sticky="news", padx=(5, 5), pady=(2, 2))
        self._overlaySelectionDropdown.grid(row=0, column=1, padx=(10, 10), pady=(2, 2), sticky="news")
        overlayFilePathLabel.grid(row=1, column=0, sticky="news", padx=(5, 5), pady=(2, 2))
        overlayFilePathSelection.grid(row=1, column=1, sticky="news", padx=(5, 5), pady=(2, 2))
        self._selectedOverlayPreview.grid(row=0, column=2, rowspan=2, sticky="news", padx=(5, 10), pady=(0, 5))

    def getFrame(self):
        return self._overlaySelectionPanel

    def getSelectedOverlayImage(self) -> tuple[str, str]:
        displayName = self._selectedOverlayVar.get()
        return (displayName, self._overlayImageManager.getImageForDisplayName(displayName))

    def loadConfiguration(self, configuration: ImageConfiguration):
        """ called when an image is selected from the list"""
        self._displayImageNameByIndex(configuration.overlayImageIndex)
        self._useOverlayVar.set(configuration.hasOverlay)

    def loadAvailableOverlayImages(self, overlayImageManager):
        self._overlayImageManager = overlayImageManager

        overlayDisplayNames = sorted(list(self._overlayImageManager.getOverlayDisplayNames().keys()))
        self._overlaySelectionDropdown.children["menu"].delete(0, tk.END)
        for overlayImage in overlayDisplayNames:
            self._overlaySelectionDropdown. \
                children["menu"]. \
                add_command(label=overlayImage,
                            command=lambda imageIndex=self._overlayImageManager.getIndexFromDisplayName(overlayImage):
                            self._newOverlaySelected(imageIndex))

        if len(overlayDisplayNames) > 0:
            self._newOverlaySelected(0)

    def _toggleUseOverlayImage(self):
        self._modificaitonElement.getCurrentImageConfig().hasOverlay = self._useOverlayVar.get()
        self._previewPanel.updateFromConfiguration()

    def _newOverlaySelected(self, imageIndex: int):
        self._displayImageNameByIndex(imageIndex)
        self._modificaitonElement.getCurrentImageConfig().overlayImageIndex = imageIndex
        self._previewPanel.updateFromConfiguration()

    def _displayImageNameByIndex(self, imageIndex: int) -> str:
        displayName = self._overlayImageManager.getDisplayNameFromIndex(imageIndex)
        self._selectedOverlayVar.set(displayName)
        fullOverlayFilePath = self._overlayImageManager.getImageForDisplayName(displayName)
        _, self._previewPhotoImage = loadImagePathToCanvas(fullOverlayFilePath, self._selectedOverlayPreview)
        self._selectedOverlayFilePathVar.set(fullOverlayFilePath)
        return displayName