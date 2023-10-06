from app.storage_handler import StorageHandler
from app.user_interface import UIWindow
import time


class PlaybackCoordinator:
    def __init__(self, storage_handler: StorageHandler, ui: UIWindow):
        self.storage_handler = storage_handler
        self.ui = ui

    def start_replay(self):
        inputs = self.storage_handler.read()
        previous_time_stamp = None
        for input in inputs:
            current_time_stamp = input.get_time_stamp()
            if previous_time_stamp is not None:
                diff = current_time_stamp - previous_time_stamp
                time.sleep(diff / 1e9)
            previous_time_stamp = current_time_stamp
            self.ui.handle_input(input)


#
