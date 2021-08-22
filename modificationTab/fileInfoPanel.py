import tkinter as tk

from Functions import trimStringToElementLength


class FileInfoPanel:

    def __init__(self, parentFrame):
        self._parentFrame = parentFrame
        self._buildUI()

    def _buildUI(self):
        self._filesPanel = tk.LabelFrame(self._parentFrame, text="Selected file")
        self._filesPanel.grid_columnconfigure(0, weight=0)
        self._filesPanel.grid_columnconfigure(1, weight=1)

        fileNameLabel = tk.Label(self._filesPanel, text="Image file:")
        maskFileNameLabel = tk.Label(self._filesPanel, text="Mask file:")

        self._imageFilePathVar = tk.StringVar()
        self._maskFilePathVar = tk.StringVar()
        self._fileNameLabelSelection = tk.Label(self._filesPanel, textvariable=self._imageFilePathVar,
                                                bg="white", width=10)
        self._maskFileLabelSelection = tk.Label(self._filesPanel, textvariable=self._maskFilePathVar,
                                                bg="white", width=10)

        fileNameLabel.grid(row=1, column=0, padx=(5, 5), pady=(2, 2))
        maskFileNameLabel.grid(row=2, column=0, padx=(5, 5), pady=(2, 2))
        self._fileNameLabelSelection.grid(row=1, column=1, sticky="news", padx=(5, 5), pady=(2, 2))
        self._maskFileLabelSelection.grid(row=2, column=1, sticky="news", padx=(5, 5), pady=(2, 2))

    def getFrame(self):
        return self._filesPanel

    def loadFilePaths(self, imagePath:str, maskPath:str):
        imageFilePathToDisplay = trimStringToElementLength(imagePath)
        self._imageFilePathVar.set(imageFilePathToDisplay)
        maskFilePathToDisplay = trimStringToElementLength(maskPath)
        self._maskFilePathVar.set(maskFilePathToDisplay)

