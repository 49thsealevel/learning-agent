import numpy as np
import pytest

from app.inputs import Screen
from app.inputs import Input
from app.inputs import Mouse
from app.inputs import Keyboard
import pickle


def test_screen():
    screen = Screen(contents=None)
    assert screen is not None
    assert type(screen) == Screen
    assert issubclass(Screen, Input)


def test_screen_contents():
    contents = np.zeros((2, 2))
    screen = Screen(contents)
    assert screen is not None
    assert np.all(np.equal(screen.contents, contents))


def test_screen_serialization():
    contents = np.zeros((2, 2))
    screen = Screen(contents)
    data = screen.serialize()
    assert data == pickle.dumps(contents)
    contents = np.ones((50, 700, 30))
    screen = Screen(contents)
    data = screen.serialize()
    assert data == pickle.dumps(contents)


def test_mouse():
    mouse = Mouse(button1=0, button2=0, direction=0, speed=0)
    assert mouse is not None
    assert type(mouse) == Mouse
    assert issubclass(Mouse, Input)


def test_mouse_contents():
    mouse = Mouse(button1=1, button2=0, direction=70.3, speed=3)
    assert mouse is not None
    assert mouse.button1 == 1
    assert mouse.button2 == 0
    assert mouse.direction == 70.3
    assert mouse.speed == 3


def test_mouse_serialization():
    mouse = Mouse(button1=0, button2=1, direction=144.6, speed=7)
    data = mouse.serialize()
    assert data == "0,1,144.6,7"


def test_keyboard():
    keyboard = Keyboard(key_change={"a": 1})
    assert keyboard is not None
    assert type(keyboard) == Keyboard
    assert issubclass(Keyboard, Input)


def test_keyboard_contents():
    keyboard = Keyboard(key_change={"space": -1})
    assert keyboard is not None
    assert "space" in keyboard.key_change
    assert keyboard.key_change["space"] == -1


def text_keyboard_serialization():
    keyboard = Keyboard(key_change={"enter": 1})
    data = keyboard.serialize()
    assert data == "enter+"
    keyboard = Keyboard(key_change={"space": -1})
    data = keyboard.serialize()
    assert data == "space-"


def test_invalid_keyboard():
    with pytest.raises(AssertionError):
        Keyboard(key_change={"t": 1, "k": -1})
    with pytest.raises(AssertionError):
        Keyboard(key_change={})
