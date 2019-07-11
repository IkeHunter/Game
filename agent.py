import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

import os
import random
import time

import game_library as gl
import game_main as gm
import game_classes as gc

env = gc.GameMethods()

games_to_play = 10

for i in range(games_to_play):
    # Reset the env
    obs = env.reset()  # initialize all vars and prep game to run
    episode_rewards = 0
    done = False

    current = obs[2]
    locations = gl.locations[current]["values"]
    action = random.choice(locations)

    while not done:
        env.render("on")  # draws frame of the game

        current = obs[2]
        locations = gl.locations[current]["values"]
        action = random.choice(locations)

        # Take a step in the env with the chosen action
        obs, reward, done, info = env.step(action)
        episode_rewards += reward
        time.sleep(5)

    print(episode_rewards)  # print total rewards when done

# env.close()  # close the env

