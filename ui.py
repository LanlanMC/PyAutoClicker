import tkinter as tk
import tkinter.ttk as ttk
from typing import Literal, Optional

import thread


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("644x400+512+512")
        self.title("PyAutoClicker")
        self.resizable(False, False)
        self.deiconify()

        # Threads
        self.left_thread: Optional[thread.LeftClickThread] = None
        self.right_thread: Optional[thread.LeftClickThread] = None

        # Variables
        self.button_text = tk.StringVar(value="开始")

        # Setup UI
        self.style = ttk.Style()
        self.style.theme_use("vista")

        self.click_interval_frame = ClickIntervalFrame(self, width=300, height=300)
        self.click_interval_frame.place(x=16, y=12)

        self.settings_frame = SettingFrame(self, width=312, height=160)
        self.settings_frame.place(x=324, y=12)

        TipsFrame(self, width=312, height=160).place(x=324, y=180)

        self.control_button = ttk.Button(self, textvariable=self.button_text, command=self.control)
        self.control_button.place(x=400, y=352)

        self.auto_tap1 = self.settings_frame.auto_tap1
        self.auto_tap2 = self.settings_frame.auto_tap2
        self.seperate_control = self.click_interval_frame.seperate_control
        self.all_interval = self.click_interval_frame.all_interval
        self.left_interval = self.click_interval_frame.left_interval
        self.right_interval = self.click_interval_frame.right_interval

        self.updater = thread.UpdaterThread(self, 0.05)
        self.updater.start()

    def _create_thread(self):
        if self.seperate_control.get():
            self.left_thread = thread.LeftClickThread(self.left_interval.get() / 1000, self.auto_tap1.get())
            self.right_thread = thread.RightClickThread(self.right_interval.get() / 1000, self.auto_tap2.get())
        else:
            self.left_thread = thread.LeftClickThread(self.all_interval.get() / 1000, self.auto_tap1.get())
            self.right_thread = thread.RightClickThread(self.all_interval.get() / 1000, self.auto_tap2.get())

        self.left_thread.start()
        self.right_thread.start()

    def _terminate_thread(self):
        if self.left_thread is not None:
            self.left_thread.terminate()
        if self.right_thread is not None:
            self.right_thread.terminate()

    def control(self):
        if self.button_text.get() == "开始":
            self._create_thread()
            self.button_text.set("停止")
            self.click_interval_frame.set_state(tk.DISABLED)
            self.settings_frame.set_state(tk.DISABLED)
        else:
            self._terminate_thread()
            self.button_text.set("开始")
            self.click_interval_frame.set_state(tk.NORMAL)
            self.settings_frame.set_state(tk.NORMAL)


class ClickIntervalFrame(ttk.LabelFrame):

    def __init__(self, master, *, width, height, labelwidget=None):
        if labelwidget is None:
            super().__init__(master, width=width, height=height, text="点击间隔")
        else:
            super().__init__(master, width=width, height=height, labelwidget=labelwidget)

        # Variables
        self.seperate_control = tk.BooleanVar(value=False)
        self.all_interval = tk.IntVar(value=100)
        self.left_interval = tk.IntVar(value=100)
        self.right_interval = tk.IntVar(value=100)

        # Define widgets
        self.all_desc_label = ttk.Label(self, text="间隔:")

        self.sep_checkbox = ttk.Checkbutton(self, variable=self.seperate_control, text="分别控制")
        self.all_spinbox = ttk.Spinbox(self, from_=0, to=5000, increment=5, textvariable=self.all_interval, width=7)
        self.interval_frame = ttk.LabelFrame(self, width=272, height=160, labelwidget=self.sep_checkbox)
        self.left_spinbox = ttk.Spinbox(self.interval_frame, from_=0, to=5000, increment=5,
                                        state=tk.NORMAL if self.seperate_control.get() else tk.DISABLED,
                                        textvariable=self.left_interval, width=7)
        self.right_spinbox = ttk.Spinbox(self.interval_frame, from_=0, to=5000, increment=5,
                                         state=tk.NORMAL if self.seperate_control.get() else tk.DISABLED,
                                         textvariable=self.right_interval, width=7)

        self.all_unit_label = ttk.Label(self, text="ms")
        self.left_unit_label = ttk.Label(self.interval_frame, text="ms",
                                         state=tk.NORMAL if self.seperate_control.get() else tk.DISABLED)
        self.right_unit_label = ttk.Label(self.interval_frame, text="ms",
                                          state=tk.NORMAL if self.seperate_control.get() else tk.DISABLED)

        self.left_desc_label = ttk.Label(self.interval_frame, text="左键:",
                                         state=tk.NORMAL if self.seperate_control.get() else tk.DISABLED)
        self.right_desc_label = ttk.Label(self.interval_frame, text="右键:",
                                          state=tk.NORMAL if self.seperate_control.get() else tk.DISABLED)

        self.hint_label = ttk.Label(self, text="过低的点击间隔(0)可能导致鼠标卡顿")

        # Place widgets
        self.all_desc_label.place(x=12, y=12)

        self.all_spinbox.place(x=64, y=12)
        self.interval_frame.place(x=12, y=68)
        self.left_spinbox.place(x=96, y=0)
        self.right_spinbox.place(x=96, y=32)

        self.all_unit_label.place(x=160, y=12)
        self.left_unit_label.place(x=192, y=0)
        self.right_unit_label.place(x=192, y=32)

        self.left_desc_label.place(x=32, y=0)
        self.right_desc_label.place(x=32, y=32)

        self.hint_label.place(x=0, y=240)

    def set_state(self, state: Literal["normal", "disabled", "active"]) -> None:
        self.all_desc_label["state"] = state
        self.all_spinbox["state"] = state
        self.all_unit_label["state"] = state
        self.set_interval_frame_state(state if self.seperate_control.get() else tk.DISABLED)
        self.sep_checkbox["state"] = state
        self.hint_label["state"] = state

    def set_interval_frame_state(self, state: Literal["normal", "disabled", "active"]) -> None:
        self.left_desc_label["state"] = state
        self.left_spinbox["state"] = state
        self.left_unit_label["state"] = state
        self.right_desc_label["state"] = state
        self.right_spinbox["state"] = state
        self.right_unit_label["state"] = state


class SettingFrame(ttk.LabelFrame):
    def __init__(self, master, *, width, height, labelwidget=None):
        if labelwidget is None:
            super().__init__(master, width=width, height=height, text="设置")
        else:
            super().__init__(master, width=width, height=height, labelwidget=labelwidget)

        # Variables
        self.auto_tap1 = tk.BooleanVar(value=False)
        self.auto_tap2 = tk.BooleanVar(value=False)

        # Define widgets
        self.auto_tap1_checkbox = ttk.Checkbutton(self, variable=self.auto_tap1, text="自动切换武器")
        self.auto_tap2_checkbox = ttk.Checkbutton(self, variable=self.auto_tap2, text="自动切换方块")

        self.auto_tap1_desc_label = ttk.Label(self, text="在左键时自动切换到武器（按下\"1\")")
        self.auto_tap2_desc_label = ttk.Label(self, text="在右键时自动切换到方块（按下\"2\")")

        # Place widgets
        self.auto_tap1_checkbox.place(x=12, y=0)
        self.auto_tap2_checkbox.place(x=12, y=64)

        self.auto_tap1_desc_label.place(x=12, y=28)
        self.auto_tap2_desc_label.place(x=12, y=92)

    def set_state(self, state: Literal["normal", "disabled", "active"]) -> None:
        self.auto_tap1_checkbox["state"] = state
        self.auto_tap1_desc_label["state"] = state
        self.auto_tap2_checkbox["state"] = state
        self.auto_tap2_desc_label["state"] = state


class TipsFrame(tk.LabelFrame):
    """此组件是常量，在运行时无变化"""

    def __init__(self, master, *, width, height, labelwidget=None):
        if labelwidget is None:
            super().__init__(master, width=width, height=height, text="提示")
        else:
            super().__init__(master, width=width, height=height, labelwidget=labelwidget)

        # Setup UI
