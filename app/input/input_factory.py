from typing import List
from app.inputs import Input


class InputFactory:
    def __init__(
        self,
    ):
        self.registry = {}

    def create(self, input_type, contents) -> List[Input]:
        return []

    def register(self, input_type, deserializer):
        pass
