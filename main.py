import argparse
from argparse import Namespace

from app.input.core import ScreenInputListener, KeyboardInputListener, MouseInputListener
from app.storage_handlers.core import FileSystemStorageHandler
from app.record_keeper import RecordKeeper


def main(args: Namespace):
    screen_input_listener = ScreenInputListener()
    keyboard_input_listener = KeyboardInputListener()
    mouse_input_listener = MouseInputListener()
    handler = FileSystemStorageHandler(path=args.path)
    record_keeper = RecordKeeper(
        input_listeners=[
            screen_input_listener,
            keyboard_input_listener,
            mouse_input_listener,
        ],
        storage_handler=handler,
        duration=1,
    )

    try:
        record_keeper.start_keeping_records()
    except Exception as e:
        print(e)
        for input_listener in record_keeper.input_listeners:
            input_listener.close()


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser()

    # Add the command line arguments
    parser.add_argument(
        "--path", required=True, help="Root directory for FilesystemStorageHandler"
    )

    # Parse the arguments
    args = parser.parse_args()
    main(args)
