from app.storage_handler import StorageHandler
from app.user_interface import UIWindow


class PlaybackCoordinator:
    def __init__(self, storage_handler: StorageHandler, ui: UIWindow):
        self.storage_handler = storage_handler
        self.ui = ui

    def start_replay(self):
        inputs = self.storage_handler.read()
        for input in inputs:
            self.ui.handle_input(input)
