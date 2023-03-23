import time
import os
from app.inputs import Input


class StorageHandler:
    def write(self, input: Input):
        raise NotImplementedError

class FileSystemStorageHandler(StorageHandler):
    def __init__(self, path: str):
        self.path = path

    def write(self, input: Input):
        directory = os.path.join(self.path, input.get_input_type().name)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        time_stamp = input.get_time_stamp()
        filename = os.path.join(directory, f"{time_stamp}.dat")

        with open(filename, "w") as f:
            f.write(input.serialize())