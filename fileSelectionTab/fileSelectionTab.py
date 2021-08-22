import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk

from fileSelectionTab.overlayImageSelection import OverlayImageSelectionPanel
from imageFileManager import ImageFileManager


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
        self._parentFrame.grid_rowconfigure(0, weight=1)
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

        self._outputFolderVar = tk.StringVar()
        outputFolderLabel = tk.Label(selectionPanel, text="Output folder: ")
        outputFolderEntry = tk.Entry(selectionPanel, textvariable=self._outputFolderVar)
        outputFolderSelectionButton = tk.Button(selectionPanel, image=self._folderIcon,
                                                command=lambda: setFolderPath(self._outputFolderVar))

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
        loadButton = tk.Button(buttonPanel, text="Load", command=self._loadIntoOverlayTab)
        loadButton.pack()

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

        fileManager = ImageFileManager(self._imageFolderVar.get(), maskFolderPath,
                                       self._overlayPanel.getOverlayImages())
        consistencyCheck = fileManager.checkFileToMapConsitency()
        if len(consistencyCheck[0]) != 0:
            print(f"[WARN] Images missing masks: {consistencyCheck[0]}")
        if len(consistencyCheck[1]) != 0:
            print(f"[WARN] Masks missing images: {consistencyCheck[1]}")
        if not consistencyCheck[2]:
            print("[ERROR] no overlay images selected")

        self._aoeGUI.getOverlayElement().ImageFileManager = fileManager

        self._aoeGUI.getOverlayElement().loadConfiguration(
            self._imageFolderVar.get(), maskFolderPath, self._outputFolderVar.get(),
            self._overlayPanel.getOverlayImages()
        )
