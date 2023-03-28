from app.input_listener import InputListener
from typing import List
from app.storage_handler import StorageHandler

import time


class RecordKeeper:
    def __init__(
        self,
        input_listeners: List[InputListener],
        storage_handler: StorageHandler,
        duration: float = 1,
    ):
        self.input_listeners = input_listeners
        self.storage_handler = storage_handler

        self.keep_running = True
        self.duration = duration

    def start_keeping_records(self):
        while self.should_keep_running():
            for input_listener in self.input_listeners:
                inputs = input_listener.get_recent_inputs()
                for j in inputs:
                    self.storage_handler.write(j)
            time.sleep(self.duration)

    def should_keep_running(self):
        return self.keep_running

    def stop(self):
        self.keep_running = False


# how would you test this? (making sure it works the way you expect it to work)

# how are we going to retreieve inputs for storage handler (the reading), using and iterator pattern, for them to be displayed
# upload to github repo
