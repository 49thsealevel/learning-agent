import base64
import json
import pickle
import platform
import time
from multiprocessing import Queue, Process
from typing import List

import numpy as np
from pynput import keyboard
from pynput.mouse import Button, Listener

from app.input.types import InputType
from app.input_listener import InputListener
from app.inputs import Input

from app.input.screen_grabber import ScreenGrabber
from app.input.screen_grabber import WindowsScreenGrabber
from app.input.screen_grabber import MacScreenGrabber

screen_grabber = ScreenGrabber()
if platform.system() == "Windows":
    screen_grabber = WindowsScreenGrabber()
elif platform.system() == "Darwin":
    screen_grabber = MacScreenGrabber()


class Screen(Input):
    def __init__(self, contents: np.ndarray, time_stamp=None):
        self.contents = contents
        self.time_stamp = time.time_ns() if time_stamp is None else time_stamp

    def serialize(self) -> str:
        serialized = pickle.dumps(self.contents)
        serialized = f"{self.time_stamp}|{serialized.hex()}"
        return serialized

    def get_input_type(self) -> InputType:
        return InputType.SCREEN

    def get_time_stamp(self) -> int:
        return self.time_stamp


class ScreenInputListener(InputListener):
    def get_recent_inputs(self) -> List[Input]:
        screen = screen_grabber.grab_screen()
        return [Screen(contents=screen)]


class Keyboard(Input):
    def __init__(self, key_change: dict[str, int], time_stamp=None):
        """
        :param key_change: Dictionary where key is button being changed,
            and value is whether pressed(1) or released (-1)
        """
        self.key_change = key_change
        self.time_stamp = time.time_ns() if time_stamp is None else time_stamp

    def serialize(self) -> str:
        self.key_change["time_stamp"] = self.time_stamp
        base64_bytes = base64.b64encode(json.dumps(self.key_change).encode("ascii"))
        return str(base64_bytes, encoding="utf-8")

    def get_input_type(self) -> InputType:
        return InputType.KEYBOARD

    def get_time_stamp(self) -> int:
        return self.time_stamp


class KeyboardInputListener(InputListener):
    def __init__(self):
        self.key_events = Queue()
        self.process = Process(target=self.start_listening, args=(self.key_events,))
        self.process.start()

    def close(self):
        self.process.kill()

    def start_listening(self, queue):
        def _add_to_queue(key, direction):
            try:
                value = key.char
            except AttributeError:
                value = str(key)
            queue.put(Keyboard(key_change={value: direction}))

        def on_press(key):
            _add_to_queue(key, 1)

        def on_release(key):
            _add_to_queue(key, -1)

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def get_recent_inputs(self) -> List[Input]:
        key_events = []
        while not self.key_events.empty():
            key_events.append(self.key_events.get_nowait())
        return key_events


class Mouse(Input):
    def __init__(self, button1: int, button2: int, x: int, y: int, time_stamp=None):
        self.button1 = button1
        self.button2 = button2
        self.x = x
        self.y = y
        self.time_stamp = time.time_ns() if time_stamp is None else time_stamp

    def serialize(self) -> str:
        return f"{self.button1},{self.button2},{self.x},{self.y},{self.time_stamp}"

    def get_input_type(self) -> InputType:
        return InputType.MOUSE

    def get_time_stamp(self) -> int:
        return self.time_stamp


class MouseInputListener(InputListener):
    def __init__(self):
        self.mouse_events = Queue()
        self.process = Process(target=self.start_listening, args=(self.mouse_events,))
        self.process.start()

    def close(self):
        self.process.kill()

    def start_listening(self, queue):
        def on_move(x, y):
            mouse_instance = Mouse(button1=0, button2=0, x=x, y=y)
            queue.put(mouse_instance)

        def on_click(x, y, button, pressed):
            if button == Button.left:
                button1 = 1 if pressed else -1
                button2 = 0
            elif button == Button.right:
                button2 = 1 if pressed else -1
                button1 = 0
            else:
                button1 = 0
                button2 = 0
            mouse = Mouse(button1=button1, button2=button2, x=x, y=y)
            queue.put(mouse)

        with Listener(on_move=on_move, on_click=on_click) as listener:
            listener.join()

    def get_recent_inputs(self) -> List[Mouse]:
        mouse_events = []
        while not self.mouse_events.empty():
            mouse_events.append(self.mouse_events.get_nowait())
        return mouse_events
