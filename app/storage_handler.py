from app.inputs import Input
from typing import List


class StorageHandler:
    def write(self, inputs: List[Input]):
        raise NotImplementedError

    def read(self) -> List[Input]:
        raise NotImplementedError
