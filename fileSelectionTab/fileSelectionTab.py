import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk

from fileSelectionTab.overlayImageSelection import OverlayImageSelectionPanel
from imageFileManager import ImageFileManager
from tooltips import BindTooltip


def setFolderPath(stringVar: tk.StringVar):
    selection = tk.filedialog.askdirectory()
    if selection:
        stringVar.set(selection)

class FileSelectionTab:

    def __init__(self, aoeGUI, parentFrame: ttk.Frame):
        self._aoeGUI = aoeGUI
        self._parentFrame = parentFrame

        self._buildUI()

    def _buildUI(self):
        self._parentFrame.grid_columnconfigure(0, weight=1)
        self._parentFrame.grid_columnconfigure(1, weight=1)
        self._parentFrame.grid_rowconfigure(0, weight=2)
        self._parentFrame.grid_rowconfigure(1, weight=2)

        self._folderIcon = tk.PhotoImage(file="./imgs/folder-icon_22.png")

        self._buildIntroPanel()
        self._buildSelectionPanel()
        self._buildButtonPanel()

    def _buildIntroPanel(self):
        self._introFrame = tk.LabelFrame(self._parentFrame)
        self._introFrame.grid(row=0, column=0, columnspan=2, sticky="news", padx=(5, 5), pady=(5, 5))

    def _buildSelectionPanel(self):
        selectionPanel = tk.LabelFrame(self._parentFrame, text="Folder Selection")
        selectionPanel.grid(row=1, column=0, sticky="news", padx=(5, 5), pady=(5, 5))
        selectionPanel.grid_columnconfigure(0, weight=0)
        selectionPanel.grid_columnconfigure(1, weight=1)
        selectionPanel.grid_columnconfigure(2, weight=0)

        self._imageFolderVar = tk.StringVar()
        imageFolderLabel = tk.Label(selectionPanel, text="Image folder: ")
        imageFolderEntry = tk.Entry(selectionPanel, textvariable=self._imageFolderVar)
        imageFolderSelectionButton = tk.Button(selectionPanel, image=self._folderIcon,
                                               command=lambda: setFolderPath(self._imageFolderVar))

        outputFolderLabel = tk.Label(selectionPanel, text="Output folder: ")
        outputFolderEntry = tk.Entry(selectionPanel, textvariable=self._aoeGUI.outputFolderPathVar)
        outputFolderSelectionButton = tk.Button(selectionPanel, image=self._folderIcon,
                                                command=lambda: setFolderPath(self._aoeGUI.outputFolderPathVar))

        maskFolderPanel = tk.LabelFrame(selectionPanel, text="Image masks")
        maskFolderPanel.grid_columnconfigure(1, weight=1)
        self._separateMaskFolderVar = tk.BooleanVar()
        self._separateMaskFolderPathVar = tk.StringVar()
        separateMaskFolderCheckbox = tk.Checkbutton(maskFolderPanel, text="Separate mask folder",
                                                    variable=self._separateMaskFolderVar,
                                                    command=self._toggleIndividualMaskFolder)
        autoGenerateMasks = tk.Button(maskFolderPanel, text="Auto generate masks", state=tk.DISABLED)
        maskFolderLabel = tk.Label(maskFolderPanel, text="Mask folder:")
        maskFolderEntry = tk.Entry(maskFolderPanel, textvariable=self._separateMaskFolderPathVar)
        self._maskFolderSelectionButton = tk.Button(maskFolderPanel, state=tk.DISABLED, image=self._folderIcon,
                                                    command=lambda: setFolderPath(self._separateMaskFolderPathVar))

        self._overlayPanel = OverlayImageSelectionPanel(self._aoeGUI, selectionPanel)

        imageFolderLabel.grid(row=0, column=0)
        imageFolderEntry.grid(row=0, column=1, sticky="ew", padx=(5, 5))
        imageFolderSelectionButton.grid(row=0, column=2)

        separateMaskFolderCheckbox.grid(row=0, column=0, padx=(5, 5))
        autoGenerateMasks.grid(row=0, column=1, padx=(5, 5))
        maskFolderLabel.grid(row=1, column=0, padx=(5, 5))
        maskFolderEntry.grid(row=1, column=1, sticky="ew", padx=(5, 5))
        self._maskFolderSelectionButton.grid(row=1, column=2, padx=(5, 5), pady=(5, 5))
        maskFolderPanel.grid(row=1, column=0, columnspan=3, stick="news", padx=(5, 5), pady=(15, 15))

        outputFolderLabel.grid(row=2, column=0, padx=(5, 5))
        outputFolderEntry.grid(row=2, column=1, sticky="ew", padx=(5, 5))
        outputFolderSelectionButton.grid(row=2, column=2, padx=(5, 5))

        self._overlayPanel.getFrame().grid(row=3, column=0, columnspan=3, sticky="news", pady=(10, 10), padx=(5, 5))

    def _buildButtonPanel(self):
        buttonPanel = tk.LabelFrame(self._parentFrame, text=" ")
        buttonPanel.grid_columnconfigure(0, weight=1)
        buttonPanel.grid_rowconfigure(5, weight=1)
        loadButton = tk.Button(buttonPanel, text="Load", command=self._loadIntoOverlayTab)

        self._imagesLoadedVar = tk.StringVar()
        self._masksLoadedVar = tk.StringVar()
        self._overlayImagesVar = tk.StringVar()
        self._loadSummaryVar = tk.StringVar()

        imagesLoadedLabel = tk.Label(buttonPanel, textvariable=self._imagesLoadedVar, width=10, anchor="w")
        masksLoadedLabel = tk.Label(buttonPanel, textvariable=self._masksLoadedVar, width=10, anchor="w")
        overlayImagesLabel = tk.Label(buttonPanel, textvariable=self._overlayImagesVar, width=10, anchor="w")
        loadSummaryLabel = tk.Label(buttonPanel, textvariable=self._loadSummaryVar, width=10, anchor="center")
        self._loadSummaryDetailTextArea = tk.Text(buttonPanel, width=10)

        loadButton.grid(row=0, column=0, pady=(10, 5))
        imagesLoadedLabel.grid(row=1, column=0, sticky="news", pady=(10, 5))
        masksLoadedLabel.grid(row=2, column=0, sticky="news", pady=(10, 5))
        overlayImagesLabel.grid(row=3, column=0, sticky="news", pady=(10, 5))
        loadSummaryLabel.grid(row=4, column=0, sticky="news", pady=(5, 5))
        self._loadSummaryDetailTextArea.grid(row=5, column=0, sticky="news", pady=(5, 5), padx=(5, 5))
        BindTooltip(self._loadSummaryDetailTextArea, "Shows issues after paths have been loaded")

        buttonPanel.grid(row=1, column=1, sticky="news", pady=(5, 5), padx=(5, 5))

    def _toggleIndividualMaskFolder(self):
        useIndividualFolder = self._separateMaskFolderVar.get()
        tkState = tk.NORMAL if useIndividualFolder else tk.DISABLED
        self._maskFolderSelectionButton.config(state=tkState)

    def _loadIntoOverlayTab(self):
        if self._separateMaskFolderVar.get():
            maskFolderPath = self._separateMaskFolderPathVar.get()
        else:
            maskFolderPath = self._imageFolderVar.get()

        if not os.path.exists(self._imageFolderVar.get()):
            tk.messagebox.showwarning("No image folder", "You need to set an image folder path")
            return

        fileManager = ImageFileManager(self._imageFolderVar.get(), maskFolderPath,
                                       self._overlayPanel.getOverlayImages())
        consistencyCheck = fileManager.checkFileToMapConsitency()
        if not self.setStatusMessagesAfterLoad(fileManager, consistencyCheck):
            return

        self._aoeGUI.getOverlayElement().ImageFileManager = fileManager

        self._aoeGUI.getOverlayElement().loadConfiguration(
            self._imageFolderVar.get(), maskFolderPath,
            self._overlayPanel.getOverlayImages()
        )

    def setStatusMessagesAfterLoad(self, fileManager, consistencyCheck) -> bool:
        consistencyCheck = fileManager.checkFileToMapConsitency()
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