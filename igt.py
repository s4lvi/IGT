import gym
import random
import stable_baselines3
from stable_baselines3.common.env_checker import check_env
import numpy as np

from gym import Env, spaces

"""
Implementation of the Iowa Gambling Task for use in reinforcement learning agents.
by JM Salvi
"""

class IGT(Env):

    def __init__(self):
        super(IGT, self).__init__()
        self.agent_bank = 2000
        self.cards = 100
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Tuple((spaces.Box(0, 5000, shape=(1,), dtype=int),spaces.Discrete(2),spaces.Box(-150, 0, shape=(1,), dtype=int),spaces.Box(0, 100, shape=(1,), dtype=int)))
        return

    def reset(self):
        self.agent_bank = 2000
        self.cards = 100
        return ([self.agent_bank], 0, [0], [self.cards])


    def step(self, action):
        reward = 0
        fee = 0
        fee_amount = 0
        self.cards -= 1
        if (action == 0 or action == 1):
            reward = 100
            if (random.randint(0,1)):
                reward = -150
                fee = 1
                fee_amount = 150
        elif (action == 2 or action == 3):
            reward = 50
            if (random.randint(0,1)):
                reward = 0
                fee = 1
                fee_amount = 50
        else: 
            raise ValueError("Received invalid action={} which is not part of the action space".format(action)) 

        self.agent_bank += reward
        done = bool(self.agent_bank <= 0 or self.cards == 0)
        info = {}
        return ([[self.agent_bank], fee, [fee_amount], [self.cards]]), reward, done, info
    
    def render(self):
        print(self.agent_bank)

env = IGT()
print(env.observation_space.sample())
# If the environment don't follow the interface, an error will be thrown
check_env(env, warn=True)