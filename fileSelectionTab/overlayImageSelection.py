import tkinter as tk
import tkinter.filedialog
import os
from PIL import Image, ImageTk
from functions.Functions import calculatePreviewImageSize, loadImagePathToCanvas


class OverlayImageSelectionPanel:
    """ In the file selection, this can preview the different overlay images """

    def __init__(self, aoeGUI, parentFrame):
        self._aoeGUI = aoeGUI
        self._parentFrame = parentFrame
        self._overlayImages = {}
        self._fileCounter = 1

        self._buildUI()

    def _buildUI(self):
        overLayPanel = tk.LabelFrame(self._parentFrame, text="Overlay images")
        self._overlayPanel = overLayPanel
        overLayPanel.grid_columnconfigure(0, weight=0)
        overLayPanel.grid_columnconfigure(1, weight=1)
        overLayPanel.grid_columnconfigure(2, weight=0)
        addOverlayImages = tk.Button(overLayPanel, text="Add image(s)", command=self._askForAdditionalOverlayPicture)
        removeOverlayImages = tk.Button(overLayPanel, text="Remove selected", command=self._removeSelectedImage)
        removeAllOverlayImages = tk.Button(overLayPanel, text="Remove all images", command=self._removeAllImages)
        self._overlayImagesList = tk.Listbox(overLayPanel)
        self._overlayImagesList.bind('<<ListboxSelect>>', self._listItemSelected)
        self._overlayImagesPreview = tk.Canvas(overLayPanel, width=100, height=100, bg="white")

        addOverlayImages.grid(row=0, column=0, padx=(5, 5))
        removeOverlayImages.grid(row=1, column=0, padx=(5, 5))
        removeAllOverlayImages.grid(row=2, column=0, padx=(5, 5))
        self._overlayImagesList.grid(row=0, column=1, rowspan=3, sticky="news", padx=(10, 10), pady=(5, 10))
        self._overlayImagesPreview.grid(row=0, column=2, rowspan=3, padx=(5, 5))

    def _askForAdditionalOverlayPicture(self):
        selections = tk.filedialog.askopenfilename(
            title="Add overlay images",
            multiple=True, filetypes=[
                ("image", "*.bmp"), ("image", "*.jpg"), ("image", "*.png"),
                ("All", "*")])
        for file in selections:
            if file not in self._overlayImages.values():
                self._addOverlayPicture(file)

    def _addOverlayPicture(self, file):
        fileName = os.path.basename(file)
        displayName = f"{self._fileCounter} - {fileName}"
        self._fileCounter += 1
        self._overlayImages[displayName] = file
        self._overlayImagesList.insert(tk.END, displayName)

    def getFrame(self):
        return self._overlayPanel

    def _listItemSelected(self, event):
        curSelection = self._overlayImagesList.curselection()
        if len(curSelection) <= 0:
            return
        selectedIndex = curSelection[0]
        displayName = self._overlayImagesList.get(selectedIndex)
        selectedFile = self._overlayImages[displayName]
        print(f"{displayName} -> {selectedFile}")
        self._previewImage(selectedFile)

    def _removeSelectedImage(self):
        curSelection = self._overlayImagesList.curselection()
        if len(curSelection) == 0:
            return
        selectedIndex = curSelection[0]
        displayName = self._overlayImagesList.get(selectedIndex)
        selectedFile = self._overlayImages[displayName]
        print(f"Removing {displayName} -> {selectedFile}")
        self._overlayImagesList.delete(selectedIndex)
        del self._overlayImages[displayName]

    def _removeAllImages(self):
        self._fileCounter = 1
        self._overlayImages.clear()
        self._overlayImagesList.delete("0", tk.END)

    def _previewImage(self, filePath):
        try:
            print(f"Preview image: {filePath}")
            self._selectedPreviewImage, self._selectedPreviewPhotoImage = \
                loadImagePathToCanvas(filePath, self._overlayImagesPreview)
        except Exception as e:
            print(e)

    def getOverlayImages(self):
        return self._overlayImages

    def loadOverlayImages(self, imageList):
        if imageList:
            for imagePath in imageList:
                self._addOverlayPicture(imagePath)



