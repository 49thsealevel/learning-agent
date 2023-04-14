import pickle
from enum import Enum, auto
import numpy as np
import time


class InputType(Enum):
    SCREEN = auto()
    KEYBOARD = auto()
    MOUSE = auto()


class Input:
    def serialize(self) -> str:
        raise NotImplementedError

    def get_input_type(self) -> InputType:
        raise NotImplementedError

    def get_time_stamp(self) -> int:
        raise NotImplementedError


class Screen(Input):
    def __init__(self, contents: np.ndarray):
        self.contents = contents
        self.time_stamp = time.time_ns()

    def serialize(self) -> str:
        # Bytestring option
        serialized = pickle.dumps(self.contents)
        # deserialized_a = pickle.loads(serialized)
        return str(serialized)

    def get_input_type(self) -> InputType:
        return InputType.SCREEN

    def get_time_stamp(self) -> int:
        return self.time_stamp


class Mouse(Input):
    def __init__(
        self,
        button1: int,
        button2: int,
        x: int,
        y: int,
    ):
        self.button1 = button1
        self.button2 = button2
        self.x = x
        self.y = y

    def serialize(self) -> str:
        return f"{self.button1},{self.button2},{self.x},{self.y}"

    def get_input_type(self) -> InputType:
        return InputType.MOUSE

    def get_time_stamp(self) -> int:
        return 0


class Keyboard(Input):
    def __init__(self, key_change: dict[str, int]):
        """
        :param key_change: Dictionary where key is button being changed,
            and value is whether pressed(1) or released (-1)
        """
        assert len(key_change) == 1
        self.key_change = key_change
        self.time_stamp = time.time_ns()

    def serialize(self) -> str:
        for key, value in self.key_change.items():
            return f'{key}{"+" if value==1 else "-"}'

    def get_input_type(self) -> InputType:
        return InputType.KEYBOARD

    def get_time_stamp(self) -> int:
        return self.time_stamp
