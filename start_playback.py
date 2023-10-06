import argparse
from argparse import Namespace
from app.user_interface import UIWindow
from app.storage_handlers.core import FileSystemStorageHandler
from app.playback_coordinator import PlaybackCoordinator


def main(args: Namespace):
    handler = FileSystemStorageHandler(path=args.path)
    ui_window = UIWindow()
    pbc = PlaybackCoordinator(storage_handler=handler, ui=ui_window)

    try:
        pbc.start_replay()
    except Exception as e:
        print(e)


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
