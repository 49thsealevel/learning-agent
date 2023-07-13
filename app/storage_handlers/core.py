import os
from typing import List

from app.input.input_factory import InputFactory
from app.input.types import InputType
from app.inputs import Input
from app.storage_handler import StorageHandler


class FileSystemStorageHandler(StorageHandler):
    def __init__(self, path: str):
        self.path = path
        self.input_factory = InputFactory()

    def write(self, inputs: List[Input]):
        if len(inputs) == 0:
            return
        filename = None
        for input in inputs:
            if filename is None:
                directory = os.path.join(self.path, input.get_input_type().name)
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                time_stamp = input.get_time_stamp()
                filename = os.path.join(directory, f"{time_stamp}.dat")
                break

        with open(filename, "w") as f:
            for input in inputs:
                f.write(input.serialize())
                f.write("\n")

    def read(self) -> List[Input]:
        inputs = []
        for input_type in InputType:
            directory = os.path.join(self.path, input_type.name)
            if not os.path.isdir(directory):
                continue
            for file in os.listdir(path=directory):
                filename = os.path.join(directory, file)
                if not os.path.isfile(filename):
                    continue
                with open(filename) as f:
                    contents = f.read()
                    inputs.extend(self.input_factory.create(input_type, contents))
        return inputs
