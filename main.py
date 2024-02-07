import ui
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = windll.shcore.GetScaleFactorForDevice(0)

app = ui.MainWindow(scale_factor=ScaleFactor)
app.mainloop()
