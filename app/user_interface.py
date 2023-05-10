from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from app.inputs import InputType, Input


class UIWindow:
    def __init__(self):
        self.canvas = None
        self._initialize()

    def _initialize(self):
        root = tk.Tk()
        root.geometry("800x800")
        root.title("GUI")
        self.canvas = tk.Frame(root, width=425, height=425)
        self.canvas.place(x=20, y=125)  # move canvas 100 pixels to the left

        button_frame = tk.Frame(root)
        button_frame.place(x=520, y=45, width=300)

        start_button = self._create_button(button_frame, "Start Time")
        offset_button = self._create_button(button_frame, "Time Stamp Offset")
        tbd_button = self._create_button(button_frame, "TBD")

        keyboard_frame = tk.Frame(root)
        keyboard_frame.place(x=500, y=600)

        def press(key):
            print(key)

        keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]"],
            ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "\\"],
            ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
        ]
        for row, key_row in enumerate(keys):
            for col, key in enumerate(key_row):
                button = tk.Button(
                    root, text=key, width=3, command=lambda key=key: press(key)
                )
                button.grid(row=row, column=col)

        root.mainloop()

    def _handle_screen(self, screen_array):
        PIL_image = Image.fromarray(np.uint8(screen_array)).convert("RGB")
        PIL_image = PIL_image.resize((400, 200))
        img = ImageTk.PhotoImage(PIL_image)
        label = Label(self.canvas, image=img)
        label.pack()

    def _create_button(self, button_frame, text):
        button = tk.Button(
            button_frame,
            text=text,
            bg="#DCE1E3",
            width=15,
            height=2,
            relief="ridge",
            bd=4,
        )
        button.pack(side=tk.TOP, pady=35)
        return button

    def handle_input(self, input: Input):
        if input.get_input_type() == InputType.SCREEN:
            self._handle_screen(input.contents)
