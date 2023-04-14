from multiprocessing import Process, Queue
import platform
from typing import List

from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key
import pyautogui

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


class ScreenInputListener(InputListener):
    def get_recent_inputs(self) -> List[Input]:
        screen = screen_grabber.grab_screen()
        return [Screen(contents=screen)]


class KeyboardInputListener(InputListener):
    def __init__(self):
        self.key_events = Queue()
        process = Process(target=self.start_listening, args=(self.key_events,))
        process.start()

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
        process = Process(target=self.start_listening, args=(self.mouse_events,))
        process.start()

    def start_listening(self, queue):
        def on_move(self):
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
