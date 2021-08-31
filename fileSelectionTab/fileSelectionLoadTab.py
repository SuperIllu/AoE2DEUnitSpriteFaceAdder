import os
import tkinter as tk
import tkinter.messagebox

from managers.imageFileManager import ImageFileManager
from functions.tooltips import BindTooltip


class FileSelectionLoadTab:
    """ When clicking the load button, not saving/loading related """

    def __init__(self, aoeGui, overlayPanel, parentFrame,
                 imageFolderVar,
                 separateMaskFolderVar, separateMaskFolderPathVar,
                 ):
        self._aoeGUI = aoeGui
        self._overlayPanel = overlayPanel
        self._parentFrame = parentFrame

        self._imageFolderVar = imageFolderVar
        self._separateMaskFolderVar = separateMaskFolderVar
        self._separateMaskFolderPathVar = separateMaskFolderPathVar
        self._buildUI()

    def _buildUI(self):
        self._loadPanelFrame = tk.LabelFrame(self._parentFrame, text=" ")
        self._loadPanelFrame.grid_columnconfigure(0, weight=1)
        self._loadPanelFrame.grid_rowconfigure(5, weight=1)
        loadButton = tk.Button(self._loadPanelFrame, text="Load", command=self._loadIntoOverlayTab)

        self._imagesLoadedVar = tk.StringVar()
        self._masksLoadedVar = tk.StringVar()
        self._overlayImagesVar = tk.StringVar()
        self._loadSummaryVar = tk.StringVar()

        imagesLoadedLabel = tk.Label(self._loadPanelFrame, textvariable=self._imagesLoadedVar, width=10, anchor="w")
        masksLoadedLabel = tk.Label(self._loadPanelFrame, textvariable=self._masksLoadedVar, width=10, anchor="w")
        overlayImagesLabel = tk.Label(self._loadPanelFrame, textvariable=self._overlayImagesVar, width=10, anchor="w")
        loadSummaryLabel = tk.Label(self._loadPanelFrame, textvariable=self._loadSummaryVar, width=10, anchor="center")
        self._loadSummaryDetailTextArea = tk.Text(self._loadPanelFrame, width=10)

        loadButton.grid(row=0, column=0, pady=(10, 5))
        imagesLoadedLabel.grid(row=1, column=0, sticky="news", pady=(10, 5))
        masksLoadedLabel.grid(row=2, column=0, sticky="news", pady=(10, 5))
        overlayImagesLabel.grid(row=3, column=0, sticky="news", pady=(10, 5))
        loadSummaryLabel.grid(row=4, column=0, sticky="news", pady=(5, 5))
        self._loadSummaryDetailTextArea.grid(row=5, column=0, sticky="news", pady=(5, 5), padx=(5, 5))
        BindTooltip(self._loadSummaryDetailTextArea, "Shows issues after paths have been loaded")

    def getFrame(self):
        return self._loadPanelFrame

    def loadAfterLoadFromFile(self):
        self._loadIntoOverlayTab()

    def _loadIntoOverlayTab(self):
        if self._separateMaskFolderVar.get():
            maskFolderPath = self._separateMaskFolderPathVar.get()
        else:
            maskFolderPath = self._imageFolderVar.get()

        if not os.path.exists(self._imageFolderVar.get()):
            tk.messagebox.showwarning("No image folder", "You need to set an image folder path")
            return

        self._fileManager = ImageFileManager(self._imageFolderVar.get(), maskFolderPath,
                                       self._overlayPanel.getOverlayImages())
        consistencyCheck = self._fileManager.checkFileToMapConsitency()
        if not self.setStatusMessagesAfterLoad(self._fileManager, consistencyCheck):
            return

        self._aoeGUI.getOverlayElement().ImageFileManager = self._fileManager

        self._aoeGUI.getOverlayElement().loadConfiguration(
            self._imageFolderVar.get(), maskFolderPath,
            self._overlayPanel.getOverlayImages()
        )

    def setStatusMessagesAfterLoad(self, fileManager, consistencyCheck) -> bool:
        noIssues = fileManager.evaluateCheckResult(consistencyCheck)

        imagesLoaded = len(fileManager.getAllImageNames())

        imagesLoadedMsg = f"Images loaded: \t\t{imagesLoaded}"
        self._imagesLoadedVar.set(imagesLoadedMsg)
        masksLoadedMsg = f"Masks loaded: \t\t{len(fileManager.getAllMaskNames())}"
        self._masksLoadedVar.set(masksLoadedMsg)
        overlaysLoadedMsg = f"Overlay images load: \t{len(self._overlayPanel.getOverlayImages().keys())}"
        self._overlayImagesVar.set(overlaysLoadedMsg)

        if noIssues:
            if imagesLoaded == 0:
                self._loadSummaryVar.set("Nothing loaded...")
                return False
            else:
                self._loadSummaryVar.set("No issues found in loading")
        else:
            self._loadSummaryVar.set("Missing images detected!")

        self._loadSummaryDetailTextArea.delete("1.0", tk.END)
        outputFolder = self._aoeGUI.outputFolderPathVar.get()
        if not outputFolder or not os.path.exists(outputFolder):
            self._loadSummaryDetailTextArea.insert(tk.END, f"Missing output folder\n\n")

        if not consistencyCheck[2]:
            self._loadSummaryDetailTextArea.insert(tk.END, "No overlay images loaded\n\n")
        if len(consistencyCheck[0]) != 0:
            missingMasks = "\n> ".join(consistencyCheck[0])
            self._loadSummaryDetailTextArea.insert(tk.END, f"No masks found for images:\n {missingMasks}\n\n")
            print(f"[WARN] Images missing masks: {consistencyCheck[0]}")
        if len(consistencyCheck[1]) != 0:
            missingImages = "\n> ".join(consistencyCheck[1])
            self._loadSummaryDetailTextArea.insert(tk.END, f"No images found for masks:\n {missingImages}\n\n")
            print(f"[WARN] Masks missing images: {consistencyCheck[1]}")

        return True
