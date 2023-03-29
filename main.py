from app.input_listener import ScreenInputListener, KeyboardInputListener
from app.storage_handler import FileSystemStorageHandler
from app.record_keeper import RecordKeeper


def main():
    screen_input_listener = ScreenInputListener()
    keyboard_input_listener = KeyboardInputListener()
    handler = FileSystemStorageHandler(path="C:\\Data")
    record_keeper = RecordKeeper(
        input_listeners=[screen_input_listener, keyboard_input_listener],
        storage_handler=handler,
        duration=5,
    )

    record_keeper.start_keeping_records()


if __name__ == "__main__":
    main()

    # define a keyboard input listener (googling, listening to keyboard events etc)
    # research relevant package(s), but try!!!
