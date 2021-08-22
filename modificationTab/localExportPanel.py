import tkinter as tk
import os
from PIL import Image

from imageFileManager import ImageFileManager


class LocalExportPanel:

    def __init__(self, parentFrame, modificationElement, previewPanel):
        self._parentFrame = parentFrame
        self._modificationElement = modificationElement
        self._previewPanel = previewPanel

        self._buildUI()

    def _buildUI(self):
        self._exportPanel = tk.LabelFrame(self._parentFrame, text="Export current image")
        self._exportPanel.grid_rowconfigure(0, weight=1)
        self._exportPanel.grid_rowconfigure(1, weight=1)
        self._exportPanel.grid_columnconfigure(0, weight=1)
        self._exportPanel.grid_columnconfigure(1, weight=1)
        exportImageButton = tk.Button(self._exportPanel, text=" Export image ", command=self.exportImage)
        exportMaskButton = tk.Button(self._exportPanel, text=" Export mask ", command=self.exportMask)
        exportImageAndMaskButton = tk.Button(self._exportPanel, text=" Export image & mask ",
                                             command=self.exportImageAndMask)

        exportImageButton.grid(row=0, column=0)
        exportMaskButton.grid(row=0, column=1)
        exportImageAndMaskButton.grid(row=1, column=0, columnspan=2)

    def getFrame(self):
        return self._exportPanel

    def exportImage(self):
        selectedFile = self._modificationElement.getSelectedFile()
        folderPath = self._modificationElement.getOutputFolderPath()
        image = self._previewPanel.getMergedImage()
        if selectedFile and folderPath and image:
            targetPath = f"{folderPath}{os.path.sep}{selectedFile[0]}"
            image.save(targetPath)

    def exportMask(self):
        selectedFile = self._modificationElement.getSelectedFile()
        if selectedFile:
            selectedMask = ImageFileManager.getMaskName(selectedFile[0])
            folderPath = self._modificationElement.getOutputFolderPath()
            mask = self._previewPanel.getMergedMask()
            if selectedMask and folderPath and mask:
                targetPath = f"{folderPath}{os.path.sep}{selectedMask}"
                mask.save(targetPath)

    def exportImageAndMask(self):
        self.exportImage()
        self.exportMask()

