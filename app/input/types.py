from enum import Enum, auto


class InputType(Enum):
    SCREEN = auto()
    KEYBOARD = auto()
    MOUSE = auto()
    GYM_STATE = auto()
    GYM_REWARD = auto()
    GYM_ACTION = auto()
