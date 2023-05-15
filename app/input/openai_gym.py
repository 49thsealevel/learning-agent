import pickle
import time
from typing import List

import gym
from gym.core import ActType, ObsType
import numpy as np

from app.input.types import InputType
from app.input_listener import InputListener
from app.input.core import ScreenInputListener
from app.input.screen_grabber import ScreenGrabber
from app.inputs import Input


class State(Input):
    def __init__(self, contents: ObsType):
        self.contents = contents

    def serialize(self) -> str:
        serialized = pickle.dumps(self.contents)
        return str(serialized)

    def get_input_type(self) -> InputType:
        return InputType.GYM_STATE

    def get_time_stamp(self) -> int:
        return time.time_ns()


class Action(Input):
    def __init__(self, action: ActType) -> None:
        self.action = action

    def serialize(self) -> str:
        pass

    def get_input_type(self) -> InputType:
        pass

    def get_time_stamp(self) -> int:
        pass


class Reward(Input):
    def __init__(self, reward: float) -> None:
        self.reward = reward

    def get_input_type(self) -> InputType:
        return InputType.GYM_REWARD

    def get_time_stamp(self) -> int:
        return time.time_ns()

    def serialize(self) -> str:
        return f"{self.get_time_stamp()}:{self.reward}"


class EnvManager:
    def __init__(self, env_name: str) -> None:
        # Setting render mode to rgb_array for screen grabber
        self.env = gym.make(env_name, render_mode="rgb_array")
        # Start current episode
        self.state = self.env.reset()

        self.screen_input_listener = ScreenInputListener(EnvScreenGrabber(self))
        self.state_input_listener = StateInputListener(self.state)
        self.reward_input_listener = RewardInputListener()

    def do_actions(self, actions: List[Action]) -> None:
        for action_input in actions:
            action = action_input.action
            state, reward, terminated, truncated, info = self.env.step(action=action)
            self.state = state
            self.state_input_listener.set_current_state(state)
            self.reward_input_listener.add_reward(reward)

    def get_input_listeners(self) -> List[InputListener]:
        return [
            self.screen_input_listener,
            self.reward_input_listener,
        ]

    def render(self) -> np.ndarray:
        return self.env.render()


class EnvScreenGrabber(ScreenGrabber):
    def __init__(self, env_manager: EnvManager) -> None:
        self.env_manager = env_manager

    def grab_screen(self) -> np.ndarray:
        return self.env_manager.render()


class RewardInputListener(InputListener):
    def __init__(self):
        self.rewards = []

    def add_reward(self, reward: float) -> None:
        self.rewards.append(Reward(reward))

    def get_recent_inputs(self) -> List[Input]:
        rewards = []
        while len(self.rewards) > 0:
            rewards.append(self.rewards.pop(0))
        return rewards


class StateInputListener(InputListener):
    def __init__(self, state: ObsType) -> None:
        self.current_state = state

    def set_current_state(self, state: ObsType):
        self.current_state = state

    def get_recent_inputs(self) -> List[Input]:
        return [State(self.current_state)]


class ActionInputListener(InputListener):
    def get_recent_inputs(self) -> List[Input]:
        pass
