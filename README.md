# Agent Trainer

## Purpose
Aside from being an interesting learning project, the goal of this project is to provide
a way to train a reinforcement learning agent on any task that can be demonstrated by a
human.

Reinforcement learning generally follows a paradigm with the following steps:
1. The agent begins in a state.  This state represents the world as the agent
perceives it.
2. The agent takes an action.  This can be from a discrete or continuous
action space.
3. The agent receives a reward for having taken that action.
4. The agent transitions to a new state.

This project will create a system that captures state information and user input
over the course of time, providing data for an RL agent to learn on.

The project will implement a UI to watch a replay of recorded time and actions
taken. The project will eventually have a placeholder for an agent that will be
trainable, and take actions.  Lastly, the activity of the agent will be monitorable
real-time in the UI.

## Implementation
The goal is to make this work cross-platform.  Initially, it should work on Windows 
and Mac. Work may additionally be done eventually to extend to Linux, although the
class structure should allow this easily.

All machine learning work will be done in PyTorch within this project, but will be 
encapsulated in specific classes for easy changeability.