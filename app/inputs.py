from app.input.types import InputType


class Input:
    def serialize(self) -> str:
        raise NotImplementedError

    def get_input_type(self) -> InputType:
        raise NotImplementedError

    def get_time_stamp(self) -> int:
        raise NotImplementedError
