import tkinter as tk

from Functions import trimStringToElementLength, loadImagePathToCanvas


class OverlaySelectionPanel:

    def __init__(self, parentFrame, previewPanel):
        self._parentFrame = parentFrame
        self._previewPanel = previewPanel
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

        useOverlayCheckbox = tk.Checkbutton(self._overlaySelectionPanel, text="Use an image", variable=self._useOverlayVar)
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
        selectedKey = self._selectedOverlayVar.get()
        return (selectedKey, self._overlayImages[selectedKey])

    def loadAvailableOverlayImages(self, overlayImages: dict):
        self._overlayImages = overlayImages

        self._overlaySelectionDropdown.children["menu"].delete(0, tk.END)
        for overlayImage in overlayImages.items():
            self._overlaySelectionDropdown. \
                children["menu"].add_command(label=overlayImage[0],
                                             command=lambda file=overlayImage[0]: self._newOverlaySelected(file))

        if len(overlayImages.keys()) > 0:
            firstOverlayImage = sorted(overlayImages.keys())[0]
            self._newOverlaySelected(firstOverlayImage)

    def _newOverlaySelected(self, overlayFileName):
        if self._useOverlayVar.get():
            self._selectedOverlayVar.set(overlayFileName)
            fullOverlayFilePath = self._overlayImages[overlayFileName]
            _, self._previewPhotoImage = loadImagePathToCanvas(fullOverlayFilePath, self._selectedOverlayPreview)
            self._previewPanel.setOverlayImage(overlayFileName, fullOverlayFilePath)
            self._selectedOverlayFilePathVar.set(fullOverlayFilePath)
