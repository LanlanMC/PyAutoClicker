import threading
import time

from pynput.mouse import Button, Listener

import mouse
import keybd

__all__ = ["LeftClickThread", "RightClickThread", "UpdaterThread"]


class LeftClickThread(threading.Thread):
    def __init__(self, click_interval: float, auto_tap: bool):
        super().__init__(name="LeftClickThread", daemon=True)

        self.click_interval = click_interval
        self.running = True
        self.pressed = False
        self.auto_tap = auto_tap
        self.last_tapped = False

    def on_click(self, /, *args):
        _, _, button, pressed = args
        if button == Button.x2:
            self.pressed = pressed

    def run(self):
        with Listener(on_click=self.on_click):
            while self.running:
                if self.pressed:
                    if self.auto_tap and not self.last_tapped:
                        keybd.keyTap('1')
                        self.last_tapped = True
                    mouse.left_click()
                else:
                    self.last_tapped = False
                if self.click_interval:
                    time.sleep(self.click_interval)

    def terminate(self):
        """终止线程"""
        self.running = False


class RightClickThread(threading.Thread):
    def __init__(self, click_interval: float, auto_tap: bool):
        super().__init__(name="RightClickThread", daemon=True)

        self.click_interval = click_interval
        self.running = True
        self.pressed = False
        self.auto_tap = auto_tap
        self.last_tapped = False

    def on_click(self, /, *args):
        _, _, button, pressed = args
        if button == Button.x1:
            self.pressed = pressed

    def run(self):
        with Listener(on_click=self.on_click):
            while self.running:
                if self.pressed:
                    if self.auto_tap and not self.last_tapped:
                        keybd.keyTap('2')
                        self.last_tapped = True
                    mouse.right_click()
                else:
                    self.last_tapped = False
                if self.click_interval:
                    time.sleep(self.click_interval)

    def terminate(self):
        """终止线程"""
        self.running = False


class UpdaterThread(threading.Thread):
    def __init__(self, parent, update_interval: float = 0.02):
        super().__init__(name="UpdaterThread", target=self.update, daemon=True)
        self.parent = parent
        self.recent = parent.seperate_control.get()
        self.state_dict = {"开始": "disabled", "停止": "normal"}
        self.update_interval = update_interval

    def update(self):
        while True:
            if self.parent.seperate_control.get() != self.recent:
                if self.parent.seperate_control.get():
                    new_state = self.state_dict[self.parent.button_text.get()] and self.parent.seperate_control.get()
                else:
                    new_state = "disabled"
                self.parent.click_interval_frame.set_interval_frame_state(new_state)
                self.recent = self.parent.seperate_control.get()
            time.sleep(self.update_interval)
