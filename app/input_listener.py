from multiprocessing import Process, Queue
import platform
import time
from typing import List

import numpy as np
from PIL import ImageGrab
from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import pyautogui

from app.inputs import Input
from app.inputs import Screen
from app.inputs import Keyboard
from app.inputs import Mouse


def grab_screen_as_numpy_array() -> np.ndarray:
    raise NotImplementedError()


if platform.system() == "Windows":
    try:
        from win32gui import FindWindow, GetWindowRect

        def grab_screen_windows() -> np.ndarray:
            window_handle = FindWindow(None, None)
            window_rect = GetWindowRect(window_handle)
            screen = np.array(ImageGrab.grab(bbox=window_rect))
            return screen

        grab_screen_as_numpy_array = grab_screen_windows
    except:
        raise Exception("Unable to perform necessary import for Windows")
elif platform.system() == "Darwin":
    try:
        import Quartz.CoreGraphics as CG
        import Quartz

        def grab_screen_mac() -> np.ndarray:
            main_display_id = Quartz.CGMainDisplayID()
            image = CG.CGDisplayCreateImage(main_display_id)
            width = CG.CGImageGetWidth(image)
            height = CG.CGImageGetHeight(image)
            bytesperrow = CG.CGImageGetBytesPerRow(image)

            pixeldata = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))
            image = np.frombuffer(pixeldata, dtype=np.uint8)
            image = image.reshape((height, bytesperrow // 4, 4))
            image = image[:, :width, :]
            return image

        grab_screen_as_numpy_array = grab_screen_mac
    except:
        raise Exception("Unable to perform necessary import for Mac")


class InputListener:
    def get_recent_inputs(self) -> List[Input]:
        raise NotImplementedError


class ScreenInputListener(InputListener):
    def get_recent_inputs(self) -> List[Input]:
        screen = grab_screen_as_numpy_array()
        return [Screen(contents=screen)]


class KeyboardInputListener(InputListener):
    def __init__(self):
        self.key_events = Queue()
        process = Process(target=self.start_listening, args=(self.key_events,))
        process.start()

    def start_listening(self, queue):
        def on_press(key):
            try:
                pressed = key.char
            except AttributeError:
                pressed = str(key)
            queue.put(Keyboard(key_change={pressed: 1}))

        def on_release(key):
            try:
                released = key.char
            except AttributeError:
                released = str(key)
            queue.put(Keyboard(key_change={released: -1}))

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def get_recent_inputs(self) -> List[Input]:
        key_events = []
        while not self.key_events.empty():
            key_events.append(self.key_events.get_nowait())
        return key_events


class MouseInputListener(InputListener):
    def __init__(self):
        self.mouse_events = Queue()
        process = Process(target=self.start_listening, args=(self.mouse_events,))
        process.start()

    def start_listening(self, queue):
        def on_movement(self):
            pass
            # if moving:

        #         x, y = pyautogui.position()
        #         positionStr = 'X: ' + str(x).rjust(4) + 'Y: ' + str(y).rjust(4)
        #         mouse_position = Mouse(direction=positionStr)
        #
        # speed =

        def on_click(x, y, button, pressed):
            pass
            # if pressed:

        #     if button == Button.left:
        #         mouse_event = (Mouse(button1=button, button2=None))
        # elif button == Button.right:
        #     mouse_event = Mouse(button1=None, button2= button)

        def on_release():
            pass

        def on_scroll(x, y, dx, dy):
            queue.put(Mouse(x=x, y=y, scroll_dx=dx, scroll_dy=dy))

        with mouse.Listener(
            on_click=on_click,
            on_movement=on_movement,
            on_release=on_release,
            on_scroll=on_scroll,
        ) as listener:
            listener.join()

    def get_recent_inputs(self) -> List[Input]:
        mouse_events = []
        while not self.mouse_events.empty():
            mouse_events.append(self.mouse_events.get_nowait())
        return mouse_events
