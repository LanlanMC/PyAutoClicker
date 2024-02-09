# -*- encoding=UTF-8 -*-
import ctypes

from ctypes import windll

__all__ = ["left_click", "right_click"]


class MouseInput(ctypes.Structure):
    """鼠标输入结构体"""
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class Input(ctypes.Structure):
    """输入结构体"""

    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MouseInput)]

    _anonymous_ = ("_input",)
    _fields_ = [("type", ctypes.c_ulong),
                ("_input", _INPUT)]


MOUSE_EVENT_LEFT_DOWN = 0x0002
MOUSE_EVENT_LEFT_UP = 0x0004
MOUSE_EVENT_RIGHT_DOWN = 0x0008
MOUSE_EVENT_RIGHT_UP = 0x0010

SendClick = windll.user32.SendInput
SendClick.argtypes = (ctypes.c_uint, ctypes.POINTER(Input), ctypes.c_int)
SendClick.restype = ctypes.c_uint


def left_click():
    """左键单击"""
    mouse_down = Input()
    mouse_down.type = 0
    mouse_down.mi.dwFlags = MOUSE_EVENT_LEFT_DOWN

    mouse_up = Input()
    mouse_up.type = 0
    mouse_up.mi.dwFlags = MOUSE_EVENT_LEFT_UP

    events = (Input * 2)()
    events[0] = mouse_down
    events[1] = mouse_up

    SendClick(2, events, ctypes.sizeof(Input))


def right_click():
    """右键单击"""
    mouse_down = Input()
    mouse_down.type = 0
    mouse_down.mi.dwFlags = MOUSE_EVENT_RIGHT_DOWN

    mouse_up = Input()
    mouse_up.type = 0
    mouse_up.mi.dwFlags = MOUSE_EVENT_RIGHT_UP

    events = (Input * 2)()
    events[0] = mouse_down
    events[1] = mouse_up

    SendClick(2, events, ctypes.sizeof(Input))
