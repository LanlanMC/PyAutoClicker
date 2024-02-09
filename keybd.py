# -*- encoding=UTF-8 -*-
import ctypes

keyboardMapping = {'1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57}


def keyDown(key: str) -> None:
    mods, vkCode = divmod(keyboardMapping[key], 0x100)

    for apply_mod, vk_mod in [(mods & 4, 0x12), (mods & 2, 0x11), (mods & 1, 0x10)]:
        if apply_mod:
            ctypes.windll.user32.keybd_event(vk_mod, 0, 0x0000, 0)
    ctypes.windll.user32.keybd_event(vkCode, 0, 0x0000, 0)
    for apply_mod, vk_mod in [(mods & 1, 0x10), (mods & 2, 0x11), (mods & 4, 0x12)]:
        if apply_mod:
            ctypes.windll.user32.keybd_event(vk_mod, 0, 0x0002, 0)


def keyUp(key: str) -> None:
    mods, vkCode = divmod(keyboardMapping[key], 0x100)

    for apply_mod, vk_mod in [(mods & 4, 0x12), (mods & 2, 0x11), (mods & 1, 0x10)]:
        if apply_mod:
            ctypes.windll.user32.keybd_event(vk_mod, 0, 0x0002, 0)
    ctypes.windll.user32.keybd_event(vkCode, 0, 0x0000, 0)
    for apply_mod, vk_mod in [(mods & 1, 0x10), (mods & 2, 0x11), (mods & 4, 0x12)]:
        if apply_mod:
            ctypes.windll.user32.keybd_event(vk_mod, 0, 0x0002, 0)


def keyTap(key: str) -> None:
    keyDown(key)
    keyUp(key)
