import tkinter as tk
import tkinter.ttk as ttk
import os


class FileListPanel:

    def __init__(self, modificationPanel, aoeGUI, parentFrame):
        self._modificationPanel = modificationPanel
        self._aoeGUI = aoeGUI
        self._parentFrame = parentFrame
        self._validFiles = {}
        self._buildUI()

    def _buildUI(self):
        self._mainPanel = tk.Frame(self._parentFrame)
        self._mainPanel.grid_columnconfigure(0, weight=1)
        self._mainPanel.grid_columnconfigure(1, weight=0)
        self._mainPanel.grid_rowconfigure(0, weight=1)

        infoPanel = tk.Frame(self._mainPanel)
        infoPanel.grid_columnconfigure(0, weight=1)
        infoPanel.grid_rowconfigure(0, weight=1)
        self._imageNumberVar = tk.StringVar()
        self._onlyPreviewVar = tk.BooleanVar()
        imageNumberLabel = tk.Label(infoPanel, textvariable=self._imageNumberVar, anchor="w")
        onlyPreviewCheckbox = tk.Checkbutton(infoPanel, variable=self._onlyPreviewVar)
        imageNumberLabel.grid(row=0, column=0, sticky="news")


        self._listBox = tk.Listbox(self._mainPanel)
        self._scrollBar = tk.Scrollbar(self._mainPanel)
        self._listBox.config(yscrollcommand=self._scrollBar.set)
        self._scrollBar.config(command=self._listBox.yview)

        self._listBox.bind('<<ListboxSelect>>', self._onFileSelected)

        self._listBox.grid(row=0, column=0, sticky="news")
        self._scrollBar.grid(row=0, column=1, sticky="news")
        infoPanel.grid(row=1, column=0, sticky="news")

    def getFrame(self):
        return self._mainPanel

    def loadImageList(self, imageFolderPath):
        self._listBox.delete(0, tk.END)
        allFiles = os.listdir(imageFolderPath)
        for file in allFiles:
            fullPath = f"{imageFolderPath}{os.path.sep}{file}"
            if not os.path.isfile(fullPath):
                continue
            if not file.lower().endswith(".bmp"):
                continue
            if file.lower().endswith("d.bmp"):
                continue
            self._validFiles[file] = fullPath

        self._imageNumberVar.set(f"Loaded images: {len(self._validFiles.keys())}")

        for file in sorted(self._validFiles.keys()):
            self._listBox.insert(tk.END, file)

    def _onFileSelected(self, event):
        selectionIndex = self._listBox.curselection()
        if len(selectionIndex) != 1:
            return
        imageSelection = self._listBox.get(selectionIndex[0])
        fullImagePath = self._validFiles.get(imageSelection, None)

        self._modificationPanel.loadImage(imageSelection, fullImagePath)


