import threading
import time

from pynput.mouse import Button, Listener

import mouse

# import keybd

__all__ = ["LeftClickThread", "RightClickThread"]


class LeftClickThread(threading.Thread):
    def __init__(self, click_interval: float):
        super().__init__(name="LeftClickThread", daemon=True)

        self.click_interval = click_interval
        print(click_interval)
        self.running = True
        self.pressed = False

    def on_click(self, /, *args):
        _, _, button, pressed = args
        if button == Button.x2:
            self.pressed = pressed

    def run(self):
        with Listener(on_click=self.on_click):
            while self.running:
                if self.pressed:
                    mouse.left_click()
                if self.click_interval:
                    time.sleep(self.click_interval)

    def terminate(self):
        """终止线程"""
        self.running = False


class RightClickThread(threading.Thread):
    def __init__(self, click_interval: float):
        super().__init__(name="RightClickThread", daemon=True)

        self.click_interval = click_interval
        self.running = True
        self.pressed = False

    def on_click(self, /, *args):
        _, _, button, pressed = args
        if button == Button.x1:
            self.pressed = pressed

    def run(self):
        with Listener(on_click=self.on_click):
            while self.running:
                if self.pressed:
                    mouse.right_click()
                if self.click_interval:
                    time.sleep(self.click_interval)

    def terminate(self):
        """终止线程"""
        self.running = False
