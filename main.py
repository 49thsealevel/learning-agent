import argparse
from argparse import Namespace

from app.input_listener import ScreenInputListener, KeyboardInputListener
from app.storage_handler import FileSystemStorageHandler
from app.record_keeper import RecordKeeper


def main(args: Namespace):
    screen_input_listener = ScreenInputListener()
    keyboard_input_listener = KeyboardInputListener()
    handler = FileSystemStorageHandler(path=args.path)
    record_keeper = RecordKeeper(
        input_listeners=[screen_input_listener, keyboard_input_listener],
        storage_handler=handler,
        duration=5,
    )

    record_keeper.start_keeping_records()


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

    # define a keyboard input listener (googling, listening to keyboard events etc)
    # research relevant package(s), but try!!!
