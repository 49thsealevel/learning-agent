from multiprocessing import Process, Queue
import platform
from typing import List

from pynput import mouse, keyboard
from pynput.mouse import Button, Listener
from pynput.keyboard import Key
import time


from app.inputs import Input
from app.inputs import Screen
from app.inputs import Keyboard
from app.inputs import Mouse
from app.io.screen_grabber import ScreenGrabber
from app.io.screen_grabber import WindowsScreenGrabber
from app.io.screen_grabber import MacScreenGrabber


screen_grabber = ScreenGrabber()
if platform.system() == "Windows":
    screen_grabber = WindowsScreenGrabber()
elif platform.system() == "Darwin":
    screen_grabber = MacScreenGrabber()


class InputListener:
    def get_recent_inputs(self) -> List[Input]:
        raise NotImplementedError

    def close(self):
        pass


class ScreenInputListener(InputListener):
    def get_recent_inputs(self) -> List[Input]:
        screen = screen_grabber.grab_screen()
        return [Screen(contents=screen)]


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
