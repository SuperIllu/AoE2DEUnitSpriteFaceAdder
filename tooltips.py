import tkinter as tk


class BindTooltip:

    def __init__(self, widget, text: str, waitTime: int = 250, wrapLength: int = 180):
        self._widget = widget
        self._text = text
        self._delay = waitTime
        self._wrapLength = wrapLength
        self._id = None
        self._tw = None

        widget.bind("<Enter>", self._enter)
        widget.bind("<Leave>", self._leave)
        widget.bind("<ButtonPress>", self._leave)

    def _enter(self, event):
        self._unschedule()
        self._id = self._widget.after(self._delay, self._showTooltip)

    def _leave(self, event):
        self._unschedule()
        self._hideTooltip()

    def _unschedule(self):
        id = self._id
        self._id = None
        if id:
            self._widget.after_cancel(id)

    def _showTooltip(self):
        x, y, cx, cy = self._widget.bbox("insert")
        x += self._widget.winfo_rootx() + 25
        y += self._widget.winfo_rooty() + 20
        self._tw = tk.Toplevel(self._widget)
        self._tw.wm_overrideredirect(True)
        self._tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self._tw, text=self._text, justify="left",
                         bg="white", relief="solid", borderwidth=1,
                         wraplength=self._wrapLength)
        label.pack()

    def _hideTooltip(self):
        tw = self._tw
        self._tw = None
        if tw:
            tw.destroy()
