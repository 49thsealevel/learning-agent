from typing import List

from app.inputs import Input


class InputListener:
    def get_recent_inputs(self) -> List[Input]:
        raise NotImplementedError

    def close(self):
        pass


