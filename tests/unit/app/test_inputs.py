import numpy as np
import pytest
import json

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
    assert data == str(pickle.dumps(contents))
    contents = np.ones((50, 700, 30))
    screen = Screen(contents)
    data = screen.serialize()
    assert data == str(pickle.dumps(contents))


def test_mouse():
    mouse = Mouse(button1=0, button2=0, x=0, y=0)
    assert mouse is not None
    assert type(mouse) == Mouse
    assert issubclass(Mouse, Input)


def test_mouse_contents():
    mouse = Mouse(button1=1, button2=0, x=70, y=3)
    assert mouse is not None
    assert mouse.button1 == 1
    assert mouse.button2 == 0
    assert mouse.x == 70
    assert mouse.y == 3


def test_mouse_serialization():
    mouse = Mouse(button1=0, button2=1, x=144, y=7)
    data = mouse.serialize()
    assert data == "0,1,144,7," + str(mouse.time_stamp)


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


# def test_keyboard_serialization():
#     keyboard = Keyboard(key_change={"enter": 1})
#     data = keyboard.serialize()
#     assert data == json.dumps({"enter": 1, "time_stamp": keyboard.get_time_stamp()}).encode()
#
#     keyboard = Keyboard(key_change={"space": -1})
#     data = keyboard.serialize()
#     assert data == json.dumps({"space": -1, "time_stamp": keyboard.get_time_stamp()}).encode()


def test_keyboard_serialization():
    key_change = {"enter": 1}
    time_stamp = 1681617667885778100

    keyboard = Keyboard(key_change=key_change)
    keyboard.time_stamp = time_stamp

    data = keyboard.serialize()
    expected_data = (
        "b'eyJlbnRlciI6IDEsICJ0aW1lX3N0YW1wIjogMTY4MTYxNzY2Nzg4NTc3ODEwMH0='"
    )

    assert data == expected_data


# def test_keyboard_serialization():
#     keyboard = Keyboard(key_change={"enter": 1})
#     data = keyboard.serialize()
#     # print data copy printed value to what you are asserting
#     assert data == "enter+"
#     keyboard = Keyboard(key_change={"space": -1})
#     data = keyboard.serialize()
#     assert data == "space-"


def test_invalid_keyboard():
    with pytest.raises(AssertionError):
        Keyboard(key_change={"t": 1, "k": -1})
    with pytest.raises(AssertionError):
        Keyboard(key_change={})
