import tkinter as tk
import threading
import time

from imageConfigManager import ImageConfiguration


class HoldBindCommand:
    _thread = None
    _runSemaphore = False

    @staticmethod
    def bindHoldCommand(element, command):
        def _run():
            HoldBindCommand._runSemaphore = True
            while HoldBindCommand._runSemaphore:
                command()
                time.sleep(0.125)

        def _stop():
            HoldBindCommand._runSemaphore = False

        element.bind("<ButtonPress-1>", lambda event: threading.Thread(target=_run).start())
        element.bind("<ButtonRelease-1>", lambda event: _stop())


class OverlayPositionControls:

    def __init__(self, parentFrame, previewPanel):
        self._parentFrame = parentFrame
        self._previewPanel = previewPanel
        self._buildUI()

    def _buildUI(self):
        self._positionPanel = tk.LabelFrame(self._parentFrame, text="Overlay image position")
        self._positionPanel.grid_columnconfigure(0, weight=1)
        self._positionPanel.grid_columnconfigure(1, weight=1)
        positionLogPanel = tk.Frame(self._positionPanel)
        positionLogPanel.grid_rowconfigure(0, weight=1)
        positionLogPanel.grid_rowconfigure(1, weight=1)
        positionModificationPanel = tk.Frame(self._positionPanel)

        positionLogPanel.grid(row=0, column=0, sticky="news")
        positionModificationPanel.grid(row=0, column=1, padx=(5, 10))

        self._overlayXPositionVar = tk.StringVar()
        self._overlayYPositionVar = tk.StringVar()
        self._overlayYPositionVar.trace("w", self._traceInput)
        self._overlayXPositionVar.trace("w", self._traceInput)
        self._overlayXPositionVar.set("0")
        self._overlayYPositionVar.set("0")

        xPosLabel = tk.Label(positionLogPanel, text="X Position")
        yPosLabel = tk.Label(positionLogPanel, text="Y Position")
        xPosValueLabel = tk.Entry(positionLogPanel, textvariable=self._overlayXPositionVar)
        yPosValueLabel = tk.Entry(positionLogPanel, textvariable=self._overlayYPositionVar)

        xPosLabel.grid(row=0, column=0)
        yPosLabel.grid(row=1, column=0)
        xPosValueLabel.grid(row=0, column=1)
        yPosValueLabel.grid(row=1, column=1)

        moveUpButton = tk.Button(positionModificationPanel, text="^", width=2, height=1)
        moveDownButton = tk.Button(positionModificationPanel, text="v", width=2, height=1)
        moveLeftButton = tk.Button(positionModificationPanel, text="<", width=2, height=1)
        moveRightButton = tk.Button(positionModificationPanel, text=">", width=2, height=1,)

        HoldBindCommand.bindHoldCommand(moveUpButton, lambda: self._moveOverlay("up"))
        HoldBindCommand.bindHoldCommand(moveDownButton, lambda: self._moveOverlay("down"))
        HoldBindCommand.bindHoldCommand(moveLeftButton, lambda: self._moveOverlay("left"))
        HoldBindCommand.bindHoldCommand(moveRightButton, lambda: self._moveOverlay("right"))

        moveUpButton.grid(row=0, column=1, padx=(2, 2), pady=(2, 2))
        moveLeftButton.grid(row=1, column=0, padx=(2, 2), pady=(2, 2))
        moveRightButton.grid(row=1, column=2, padx=(2, 2), pady=(2, 2))
        moveDownButton.grid(row=2, column=1, padx=(2, 2), pady=(2, 2))

    def loadConfiguration(self, configuration: ImageConfiguration):
        configurationOffset = configuration.offset
        if configurationOffset:
            self._overlayXPositionVar.set(configurationOffset[0])
            self._overlayYPositionVar.set(configurationOffset[1])
        # outside of if: will save the offset, even if the position was not updated (just previewed)
        self._updateOverlayPosition()

    def getFrame(self):
        return self._positionPanel

    def _moveOverlay(self, direction):
        newPosition = self._previewPanel.moveOverlay(direction)
        if newPosition:
            self._overlayXPositionVar.set(newPosition[0])
            self._overlayYPositionVar.set(newPosition[1])

    def _traceInput(self, a, b, c):
        self._updateOverlayPosition()

    def _updateOverlayPosition(self):
        """ forwards the infomraiton to the pnale with the preview & config upated """
        try:
            xPos = int(self._overlayXPositionVar.get())
            yPos = int(self._overlayYPositionVar.get())
            self._previewPanel.setOverlayPosition((xPos, yPos))
        except:
            position = self._previewPanel.getOverlayOffset()
            self._overlayXPositionVar.set(position[0])
            self._overlayYPositionVar.set(position[1])
