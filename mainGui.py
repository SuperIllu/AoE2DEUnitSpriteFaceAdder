import tkinter as tk
import tkinter.ttk as ttk

from persistenceManager import addPersistanceInterfaceToMenu
from fileSelectionTab.fileSelectionTab import FileSelectionTab
from modificationTab.modificationElement import ModificationElement


class AoeUnitGui:

    def __init__(self):
        self._buildUI()
        self._setIcon()
        self._buildMenu()
        self._startUI()

    def _buildUI(self):
        self._main = tk.Tk()
        self._main.title("CHUM (CHonk's Unit Modifier)")
        self._main.geometry("875x715")
        self._main.grid_columnconfigure(0, weight=1)
        self._main.grid_rowconfigure(0, weight=0)
        self._main.grid_rowconfigure(1, weight=1)

        self._titleLabel = tk.Label(self._main, text="Aaaaaa")
        self._tabs = ttk.Notebook(self._main)
        self._tabs.grid(row=1, column=0, sticky="news")

        self._filesTab = ttk.Frame(self._tabs)
        self._overlayTab = ttk.Frame(self._tabs)
        self._tabs.add(self._filesTab, text="Files")
        self._tabs.add(self._overlayTab, text="Overlay")

        self.outputFolderPathVar = tk.StringVar()

        self._fileSelectionElement = FileSelectionTab(self, self._filesTab)
        self._overlayElement = ModificationElement(self, self._overlayTab)

    def _setIcon(self):
        try:
            self._icon = tk.PhotoImage(file="./imgs/piggie_cut_mug_32.png")
            self._main.iconphoto(False, self._icon)
        except Exception:
            pass

    def _buildMenu(self):
        addPersistanceInterfaceToMenu(self)

    def getMain(self):
        """ returns tk.Tk(), mainly for keybinds """
        return self._main

    def getTabs(self):
        """ returns the notebook (tab manager) """
        return self._tabs

    def getFileSelectionElement(self):
        return self._fileSelectionElement

    def getOverlayElement(self):
        return self._overlayElement

    def _startUI(self):
        self._main.mainloop()
