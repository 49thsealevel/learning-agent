import base64
import json
import pickle
from typing import List

from app.input.core import Screen, Keyboard, Mouse
from app.input.types import InputType
from app.inputs import Input


class InputFactory:
    def __init__(
        self,
    ):
        self.registry = {
            InputType.SCREEN: create_screen,
            InputType.KEYBOARD: create_keyboard,
            InputType.MOUSE: create_mouse,
        }

    def create(self, input_type: InputType, contents: str) -> List[Input]:
        creator_function = self.registry[input_type]
        return creator_function(contents)

    def register(self, input_type, deserializer):
        pass


def create_screen(contents: str) -> List[Input]:
    for i, ch in enumerate(contents):
        if ch == "|":
            time_stamp = int(contents[0:i])
            contents = contents[i + 1 :]
            return [
                Screen(
                    contents=pickle.loads(bytes.fromhex(contents)),
                    time_stamp=time_stamp,
                )
            ]
    return []


def create_keyboard(contents: str) -> List[Input]:
    keyboard_inputs = []
    for line in contents.strip().splitlines():
        key_change = json.loads(
            base64.b64decode(bytes(line, encoding="utf-8")).decode("ascii")
        )
        keyboard_inputs.append(
            Keyboard(
                key_change=key_change,
                time_stamp=int(key_change["time_stamp"]),
            )
        )
    return keyboard_inputs


def create_mouse(contents: str) -> List[Input]:
    mouse_inputs = []
    for line in contents.strip().splitlines():
        button1, button2, x, y, time_stamp = tuple(line.split(","))
        mouse_inputs.append(
            Mouse(
                button1=int(button1),
                button2=int(button2),
                x=int(x),
                y=int(y),
                time_stamp=int(time_stamp),
            )
        )
    return mouse_inputs
