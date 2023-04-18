from app.record_keeper import RecordKeeper
from unittest.mock import MagicMock
import pytest


@pytest.mark.parametrize(
    "num_of_inputs, num_of_listeners", [(0, 1), (1, 1), (5, 1), (0, 2), (1, 2), (5, 3)]
)
def test_record_keeper_with_input(num_of_inputs: int, num_of_listeners: int):
    input_mock = MagicMock()
    input_listener_mock = MagicMock()
    input_listener_mock_list = []
    input_list = []
    for i in range(num_of_inputs):
        input_list.append(input_mock)
    input_listener_mock.get_recent_inputs.return_value = input_list
    for i in range(num_of_listeners):
        input_listener_mock_list.append(input_listener_mock)
    storage_handler_mock = MagicMock()
    record_keeper = RecordKeeper(
        input_listeners=input_listener_mock_list,
        storage_handler=storage_handler_mock,
    )
    record_keeper.test_continue = False

    def test_keep_running():
        record_keeper.test_continue = not record_keeper.test_continue
        return record_keeper.test_continue

    record_keeper.should_keep_running = test_keep_running
    record_keeper.start_keeping_records()
    assert storage_handler_mock.write.call_count == num_of_listeners
    storage_handler_mock.write.assert_called_with(input_list)
    assert len(storage_handler_mock.write.call_args_list) == num_of_listeners
    for args in storage_handler_mock.write.call_args_list:
        assert len(args[0][0]) == num_of_inputs


def test_record_keeper_no_input_listener():
    storage_handler_mock = MagicMock()
    record_keeper = RecordKeeper(
        input_listeners=[],
        storage_handler=storage_handler_mock,
    )
    record_keeper.test_continue = False

    def test_keep_running():
        record_keeper.test_continue = not record_keeper.test_continue
        return record_keeper.test_continue

    record_keeper.should_keep_running = test_keep_running
    record_keeper.start_keeping_records()
    storage_handler_mock.write.assert_not_called()
