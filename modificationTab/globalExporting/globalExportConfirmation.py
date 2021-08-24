import tkinter as tk
import types


class GlobalExportConfirmation:

    def __init__(self, totalImages: int, modifiedImages: int, exportAllCallback, exportModifiedCallback):
        self._exportAllCallback = exportAllCallback
        self._exportModifiedCallback = exportModifiedCallback

        self._message = f"Only {modifiedImages} of {totalImages} images have been modified.\n" \
                        f"Would you like to export the\nremaining {totalImages - modifiedImages} unmodified?"

        self._buildUI()

    def _buildUI(self):
        self._main = tk.Toplevel()
        self._main.title("Export confirmation")
        self._main.geometry("360x125")

        self._main.grid_columnconfigure(0, weight=1)
        self._main.grid_rowconfigure(0, weight=1)

        textfield = tk.Label(self._main, text=self._message, font=("Arial", 11))

        buttonPanel = tk.Frame(self._main)
        buttonPanel.grid_columnconfigure(0, weight=1)
        buttonPanel.grid_columnconfigure(1, weight=1)
        buttonPanel.grid_columnconfigure(2, weight=1)
        exportAll = tk.Button(buttonPanel, text=" Export all ",
                              command=lambda: self._closeAndCall(self._exportAllCallback))
        exportModified = tk.Button(buttonPanel, text=" Export only modified ",
                                   command=lambda: self._closeAndCall(self._exportModifiedCallback))
        cancel = tk.Button(buttonPanel, text=" Cancel ", command=self._main.destroy)

        exportAll.grid(row=0, column=0)
        exportModified.grid(row=0, column=1)
        cancel.grid(row=0, column=2)

        textfield.grid(row=0, column=0, sticky="news", padx=(10, 10), pady=(10, 10))
        buttonPanel.grid(row=1, column=0, sticky="news", pady=(10, 10), padx=(10, 10))

    def _closeAndCall(self, callback):
        callback()
        self._main.destroy()


if __name__ == "__main__":
    GlobalExportConfirmation(1220, 122, None, None)._main.mainloop()
