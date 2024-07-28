import os.path
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk as ttk
import webbrowser
from idlelib.tooltip import Hovertip

from fileSelectionTab.fileSelectionLoadTab import FileSelectionLoadTab
from fileSelectionTab.overlayImageSelection import OverlayImageSelectionPanel
from functions.tooltips import BindTooltip


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
        self._parentFrame.grid_rowconfigure(0, weight=0)
        self._parentFrame.grid_rowconfigure(1, weight=1)

        self._folderIcon = tk.PhotoImage(file="./imgs/folder-icon_22.png")
        self._autoOutputImage = tk.PhotoImage(file="./imgs/btn_white_dig_refresh_22.png")

        self._buildIntroPanel()
        self._buildSelectionPanel()
        self._buildButtonPanel()

    def _buildIntroPanel(self):
        url = "https://github.com/SuperIllu/AoE2DEUnitSpriteFaceAdder"

        def _openGithub():
            webbrowser.open_new(url)

        self._introFrame = tk.LabelFrame(self._parentFrame)
        self._introFrame.grid_columnconfigure(0, weight=1)
        self._introFrame.grid_columnconfigure(1, weight=1)
        self._introFrame.grid_rowconfigure(0, weight=1)
        self._introFrame.grid_rowconfigure(1, weight=1)
        self._introFrame.grid_rowconfigure(2, weight=1)
        self._introFrame.grid_rowconfigure(3, weight=1)

        self._introFrame.grid(row=0, column=0, columnspan=2, sticky="news", padx=(5, 5), pady=(5, 10))

        intro_label = tk.Label(self._introFrame,
                          text="CHUM is a tool intended to help you overlay your face over units in AoE2:DE.")
        latest_news_label = tk.Label(self._introFrame,
                          text="You can find the code and latest releases here:")
        gitlab_link_label = tk.Label(self._introFrame,
                          text="github", fg="blue", cursor="hand2")
        gitlab_link_label.bind("<Button-1>", lambda e: _openGithub())
        BindTooltip(gitlab_link_label, url, wrapLength=350)
        happy_mod_label = tk.Label(self._introFrame, text="Happy modifying")

        intro_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=(2, 0))
        latest_news_label.grid(row=1, column=0, columnspan=1, sticky="nes")
        gitlab_link_label.grid(row=1, column=1, sticky="nws")
        happy_mod_label.grid(row=2, column=0, columnspan=2, sticky="news", pady=(0, 2))

    def _buildSelectionPanel(self):
        # configure own layout to place elements
        self._selectionPanel = tk.LabelFrame(self._parentFrame, text="Folder Selection")
        self._selectionPanel.grid(row=1, column=0, sticky="news", padx=(5, 5), pady=(5, 5))
        self._selectionPanel.grid_columnconfigure(0, weight=0)
        self._selectionPanel.grid_columnconfigure(1, weight=1)
        self._selectionPanel.grid_columnconfigure(2, weight=0)

        #create elements
        self._build_source_folder_frame()
        outputFolderFrame = self._build_output_folder_frame()
        maskFolderPanel = self._build_mask_folder_frame()
        self._overlayPanel = OverlayImageSelectionPanel(self._aoeGUI, self._selectionPanel)

        # place elements
        maskFolderPanel.grid(row=1, column=0, columnspan=3, sticky="news", padx=(5, 5), pady=(15, 15))
        outputFolderFrame.grid(row=2, column=0, columnspan=3, sticky="news", padx=(5, 5), pady=(3, 3))
        self._overlayPanel.getFrame().grid(row=3, column=0, columnspan=3, sticky="news", pady=(10, 10), padx=(5, 5))

    def _build_source_folder_frame(self):
        self._imageFolderVar = tk.StringVar()
        imageFolderLabel = tk.Label(self._selectionPanel, text="Image folder: ")
        imageFolderEntry = tk.Entry(self._selectionPanel, textvariable=self._imageFolderVar)
        imageFolderSelectionButton = tk.Button(self._selectionPanel, image=self._folderIcon,
                                               command=lambda: setFolderPath(self._imageFolderVar,
                                                                             "Select image folder"))
        imageFolderLabel.grid(row=0, column=0)
        imageFolderEntry.grid(row=0, column=1, sticky="ew", padx=(5, 5))
        imageFolderSelectionButton.grid(row=0, column=2)

    def _build_mask_folder_frame(self):
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
        separateMaskFolderCheckbox.grid(row=0, column=0, padx=(5, 5))
        autoGenerateMasks.grid(row=0, column=1, padx=(5, 5))
        maskFolderLabel.grid(row=1, column=0, padx=(5, 5))
        maskFolderEntry.grid(row=1, column=1, sticky="ew", padx=(5, 5))
        self._maskFolderSelectionButton.grid(row=1, column=2, padx=(5, 5), pady=(5, 5))
        return maskFolderPanel

    def _build_output_folder_frame(self):

        def auto_generate_output_folder():
            source_path = self._imageFolderVar.get()
            if source_path and os.path.isdir(source_path):
                output_path = source_path + "_out"
                self._aoeGUI.outputFolderPathVar.set(output_path)

        outputFolderFrame = tk.LabelFrame(self._selectionPanel, text="Output folder")
        outputFolderFrame.grid_columnconfigure(1, weight=1)
        outputFolderLabel = tk.Label(outputFolderFrame, text="Path: ")
        outputFolderEntry = tk.Entry(outputFolderFrame, textvariable=self._aoeGUI.outputFolderPathVar)
        outputFolderAutoButton = tk.Button(outputFolderFrame,
                                           image=self._autoOutputImage, command=auto_generate_output_folder)
        autoAutoputTooltip = Hovertip(outputFolderAutoButton, "Auto generate path")
        outputFolderSelectionButton = tk.Button(outputFolderFrame, image=self._folderIcon,
                                                command=lambda: setFolderPath(self._aoeGUI.outputFolderPathVar,
                                                                              "Select output folder"))
        outputFolderLabel.grid(row=0, column=0, padx=(5, 5))
        outputFolderEntry.grid(row=0, column=1, sticky="ew", padx=(5, 5))
        outputFolderAutoButton.grid(row=0, column=2)
        outputFolderSelectionButton.grid(row=0, column=3, padx=(5, 5))
        return outputFolderFrame

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
                "overlayImages": self._overlayPanel.getOverlayImageManager().serialiseState()
                }

    def deserialiseState(self, state: dict):
        self._imageFolderVar.set(state.get("imageFolder", None))
        separateMasks = state.get("separateMasks", (False, None))
        self._separateMaskFolderVar.set(separateMasks[0])
        self._separateMaskFolderPathVar.set(separateMasks[1])
        self._aoeGUI.outputFolderPathVar.set(state.get("outputFolder", None))
        self._overlayPanel.loadOverlayImages(state.get("overlayImages", None))
        self._loadTab.loadAfterLoadFromFile()

