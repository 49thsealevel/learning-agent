import pickle
from typing import List

from app.input.core import Screen
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
    return []


def create_mouse(contents: str) -> List[Input]:
    return []
