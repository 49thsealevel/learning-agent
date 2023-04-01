import numpy as np
import pytest

from app.inputs import Screen
from app.inputs import Mouse
from app.inputs import Keyboard
from app.record_keeper import RecordKeeper
from unittest.mock import MagicMock


def test_record_keeper_with_empty_input():
    input_listener_mock = MagicMock()
    input_listener_mock.get_recent_inputs.return_value = []
    storage_handler_mock = MagicMock()
    record_keeper = RecordKeeper(
        input_listeners=[input_listener_mock],
        storage_handler=storage_handler_mock,
    )
    record_keeper.test_continue = False

    def test_keep_running():
        record_keeper.test_continue = not record_keeper.test_continue
        return record_keeper.test_continue

    record_keeper.should_keep_running = test_keep_running
    record_keeper.start_keeping_records()
    storage_handler_mock.write.assert_not_called()
    input_listener_mock.get_recent_inputs.assert_called_once()


def test_record_keeper_with_input():
    expected_val = "Knock knock. Who's there?"
    input_mock = MagicMock()
    input_mock.serialize.return_value = expected_val
    input_listener_mock = MagicMock()
    input_listener_mock.get_recent_inputs.return_value = [input_mock, input_mock]
    storage_handler_mock = MagicMock()
    record_keeper = RecordKeeper(
        input_listeners=[input_listener_mock],
        storage_handler=storage_handler_mock,
    )
    record_keeper.test_continue = False

    def test_keep_running():
        record_keeper.test_continue = not record_keeper.test_continue
        return record_keeper.test_continue

    record_keeper.should_keep_running = test_keep_running
    record_keeper.start_keeping_records()
    assert storage_handler_mock.write.call_count == 2
    storage_handler_mock.write.assert_called_with(expected_val)
    input_listener_mock.get_recent_inputs.assert_called_once()


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
