import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk

from fileSelectionTab.fileSelectionLoadTab import FileSelectionLoadTab
from fileSelectionTab.overlayImageSelection import OverlayImageSelectionPanel
from imageFileManager import ImageFileManager
from tooltips import BindTooltip


def setFolderPath(stringVar: tk.StringVar, title: str="Select folder"):
    selection = tk.filedialog.askdirectory(title=title)
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
        self._selectionPanel = tk.LabelFrame(self._parentFrame, text="Folder Selection")
        self._selectionPanel.grid(row=1, column=0, sticky="news", padx=(5, 5), pady=(5, 5))
        self._selectionPanel.grid_columnconfigure(0, weight=0)
        self._selectionPanel.grid_columnconfigure(1, weight=1)
        self._selectionPanel.grid_columnconfigure(2, weight=0)

        self._imageFolderVar = tk.StringVar()
        imageFolderLabel = tk.Label(self._selectionPanel, text="Image folder: ")
        imageFolderEntry = tk.Entry(self._selectionPanel, textvariable=self._imageFolderVar)
        imageFolderSelectionButton = tk.Button(self._selectionPanel, image=self._folderIcon,
                                               command=lambda: setFolderPath(self._imageFolderVar,
                                                                             "Select image folder"))

        outputFolderLabel = tk.Label(self._selectionPanel, text="Output folder: ")
        outputFolderEntry = tk.Entry(self._selectionPanel, textvariable=self._aoeGUI.outputFolderPathVar)
        outputFolderSelectionButton = tk.Button(self._selectionPanel, image=self._folderIcon,
                                                command=lambda: setFolderPath(self._aoeGUI.outputFolderPathVar,
                                                                              "Select output folder"))

        maskFolderPanel = tk.LabelFrame(self._selectionPanel, text="Image masks")
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
                                                    command=lambda: setFolderPath(self._separateMaskFolderPathVar,
                                                                                  "Select separate mask folder"))

        self._overlayPanel = OverlayImageSelectionPanel(self._aoeGUI, self._selectionPanel)

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
        self._loadTab = FileSelectionLoadTab(self._aoeGUI, self._overlayPanel, self._parentFrame,
                                             self._imageFolderVar,
                                             self._separateMaskFolderVar, self._separateMaskFolderPathVar)
        self._loadTab.getFrame().grid(row=1, column=1, sticky="news", pady=(5, 5), padx=(5, 5))

    def _toggleIndividualMaskFolder(self):
        useIndividualFolder = self._separateMaskFolderVar.get()
        tkState = tk.NORMAL if useIndividualFolder else tk.DISABLED
        self._maskFolderSelectionButton.config(state=tkState)

    def serialiseState(self):
        return {"imageFolder": self._imageFolderVar.get(),
                "separateMasks": (self._separateMaskFolderVar.get(), self._separateMaskFolderPathVar.get()),
                "outputFolder": self._aoeGUI.outputFolderPathVar.get(),
                "overlayImages": list(self._overlayPanel.getOverlayImages().values())
                }

    def deserialiseState(self, state: dict):
        self._imageFolderVar.set(state.get("imageFolder", None))
        separateMasks = state.get("separateMasks", (False, None))
        self._separateMaskFolderVar.set(separateMasks[0])
        self._separateMaskFolderPathVar.set(separateMasks[1])
        self._aoeGUI.outputFolderPathVar.set(state.get("outputFolder", None))
        self._overlayPanel.loadOverlayImages(state.get("overlayImages", None))

