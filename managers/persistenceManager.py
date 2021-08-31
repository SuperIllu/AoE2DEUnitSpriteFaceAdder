import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import json


class PersistenceManager:

    def __init__(self, mainGui):
        self._mainGui = mainGui
        self._currentConfiguration: str = None

    def saveNewConfiguration(self):
        """ always ask where to store the content """
        selection = tk.filedialog. \
            asksaveasfilename(title="Save CHUM configuration")
        if selection:
            self._currentConfiguration = selection
            self._saveToFilePath(selection)

    def overrideCurrentConfiguration(self):
        """ only asks where to store, if no previous file is set """
        if not self._currentConfiguration:
            self.saveNewConfiguration()
        else:
            self._saveToFilePath(self._currentConfiguration)

    def loadConfiguration(self):
        selection = tk.filedialog. \
            askopenfilename(title="Load CHUM configuration",
                            filetypes=[("json", "*.json"), ("All files", "*")]
                            )
        if selection:
            self._currentConfiguration = selection
            self._loadConfiguration(selection)


    def _loadConfiguration(self, filePath):
        try:
            with open(filePath, "r") as file:
                state = json.load(file)
                fileSelectionState = state.get("files", None)
                self._mainGui.getFileSelectionElement().deserialiseState(fileSelectionState)
        except Exception:
            tk.messagebox.showwarning("Loading failed", "Could not load the selected file!")

    def _saveToFilePath(self, filePath):
        state = self._assembleConfiguration()
        if not filePath.lower().endswith(".json"):
            filePath = f"{filePath}.json"
        with open(filePath, "w") as file:
            json.dump(state, file)

    def _assembleConfiguration(self):
        fileState = self._mainGui.getFileSelectionElement().serialiseState()
        configState = self._mainGui.getOverlayElement().serialiseState()

        return {"files": fileState, "configs": configState}


def addPersistanceInterfaceToMenu(gui) -> PersistenceManager:
    persistanceManager = PersistenceManager(gui)
    menuBar = tk.Menu(gui.getMain())
    fileMenu = tk.Menu(menuBar, tearoff=0)
    fileMenu.add_command(label="Load", command=persistanceManager.loadConfiguration)
    fileMenu.add_command(label="Save", command=persistanceManager.overrideCurrentConfiguration)
    fileMenu.add_command(label="Save as", command=persistanceManager.saveNewConfiguration)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=gui.getMain().destroy)
    menuBar.add_cascade(label="File", menu=fileMenu)
    gui.getMain().config(menu=menuBar)
    return persistanceManager
