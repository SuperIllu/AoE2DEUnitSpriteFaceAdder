import os
import threading
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

from fileSelectionTab.fileSelectionTab import setFolderPath
from imageConfigManager import ImageConfigurationManager
from imageFileManager import ImageFileManager


class GlobalExportPanel:
    def __init__(self, modificationElement, parentFrame):
        self._modificationElement = modificationElement
        self._parentFrame = parentFrame
        self._buildUI()

    def _buildUI(self):
        self._globalExportPanel = tk.LabelFrame(self._parentFrame, text="All files")
        self._globalExportPanel.grid_rowconfigure(1, weight=1)
        self._globalExportPanel.grid_columnconfigure(1, weight=1)

        filePathLabel = tk.Label(self._globalExportPanel, text="Output folder:")
        filePathSelection = tk.Label(self._globalExportPanel, width=10, anchor="e",
                                     textvariable=self._modificationElement.masterGUI.outputFolderPathVar, bg="white")
        self._folderIcon = tk.PhotoImage(file="./imgs/folder-icon_22.png")
        outputFolderSelectionButton = tk.Button(self._globalExportPanel, image=self._folderIcon,
                                                command=self._updateOutputFolder)

        exportAllButton = tk.Button(self._globalExportPanel, text="Export all", command=self._exportAll)
        infoLabel = tk.Label(self._globalExportPanel, text="This will override all files in the output folder",
                             font=("Arial", 10))
        self._progressBar = ttk.Progressbar(self._globalExportPanel)

        filePathLabel.grid(row=0, column=0, sticky="news", padx=(5, 5), pady=(5, 5))
        filePathSelection.grid(row=0, column=1, sticky="news", padx=(5, 5), pady=(5, 5))
        outputFolderSelectionButton.grid(row=0, column=2, padx=(2, 5), pady=(5, 5))
        infoLabel.grid(row=1, column=1, sticky="news", padx=(5, 5), pady=(5, 5))
        exportAllButton.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))
        self._progressBar.grid(row=2, column=0, columnspan=3, sticky="news", pady=(2, 2), padx=(5, 5))

    def _updateOutputFolder(self):
        setFolderPath(self._modificationElement.masterGUI.outputFolderPathVar)

    def getFrame(self):
        return self._globalExportPanel

    def _exportAllThreading(self):
        imageFileManager: ImageFileManager = self._modificationElement.ImageFileManager
        configManager: ImageConfigurationManager = self._modificationElement.ImageConfigManager
        sortedImageNames = sorted(imageFileManager.getAllImageNames())

        processedImages = 0
        totalImages = len(sortedImageNames)
        for image in sortedImageNames:
            self._exportSingleImage(image)
            processedImages += 1
            progress = 100*(processedImages / totalImages)
            self._progressBar["value"] = progress
        tk.messagebox.showinfo("Export finished", "Images and masks have been exported!")


    def _exportAll(self):
        self._progressBar["value"] = 0

        if not self._modificationElement.getOutputFolderPath():
            tk.messagebox.showwarning("Missing configuration", "No output folder selected")
            return

        imageFileManager: ImageFileManager = self._modificationElement.ImageFileManager
        configManager: ImageConfigurationManager = self._modificationElement.ImageConfigManager
        allImageNames = imageFileManager.getAllImageNames()
        imagesWithoutConfig = \
            [imageName for imageName in allImageNames if not configManager.hasConfiguration(imageName)]
        if len(imagesWithoutConfig) > 0:
            message = f"{len(imagesWithoutConfig)} do not have an overlay configuration. " \
                      f"They will be exported without changes.\n" \
                      f"Continue?"
            if tk.messagebox.askokcancel("Missing configuration", message):
                self._startExporting()
        else:
            self._startExporting()

    def _startExporting(self):
        threading.Thread(target=self._exportAllThreading).start()

    def _exportSingleImage(self, imageName: str):
        imageFileManager: ImageFileManager = self._modificationElement.ImageFileManager
        configManager: ImageConfigurationManager = self._modificationElement.ImageConfigManager

        maskName = imageFileManager.getMaskName(imageName)
        imageToExport, maskToExport = configManager.generateImagesToExport(imageName)
        outputFolderPath = self._modificationElement.getOutputFolderPath()

        imageExportPath = f"{outputFolderPath}{os.path.sep}{imageName}"
        maskExportPath = f"{outputFolderPath}{os.path.sep}{maskName}"

        imageToExport.save(imageExportPath)
        maskToExport.save(maskExportPath)
