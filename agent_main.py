import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

import os
import random

import game_classes as gc
from agent_random import random_agent
from agent_class import Agent
import game_library as gl

tf.reset_default_graph()

env = gc.GameMethods()

num_actions = 4
state_size = 2

index = 1

path = "./text_adventure_{}/".format(index)  # for checkpoints

training_episodes = 100000  # 1000
max_steps_per_episode = 1000  # 5000
episode_batch_size = 5

agent = Agent(num_actions, state_size)

init = tf.global_variables_initializer()

saver = tf.train.Saver(max_to_keep=2)

if not os.path.exists(path):
    os.makedirs(path)

with tf.Session() as sess:
    sess.run(init)

    total_episode_rewards = []

    gradient_buffer = sess.run(tf.trainable_variables())

    for index, gradient in enumerate(gradient_buffer):
        gradient_buffer[index] = gradient * 0

    for episode in range(training_episodes):
        state_all = env.reset()

        state = state_all[3]
        new_state = [state]
        # print("state: {}, state.shape: {}".format(str(state), str(state.shape)))

        agent.num_actions = 3

        episode_history = []
        episode_rewards = 0

        for step in range(max_steps_per_episode):

            if (episode % 5000 == 0) and (episode is not 0):
                print("Currently on episode " + str(episode))
                training_current = env.render("on")
            else:
                training_current = env.render("off")

            if (step % 1000 == 0) and (step is not 0):
                print("Currently on step " + str(step))

            # current = training_current
            # locations = []
            # for j in gl.locations[current]["direction_values"]:
            #     locations.append(j)

            locations = []
            for i in gl.directions:
                locations.append(i)

            locations = np.array(locations)

            action_probabilities = sess.run(agent.outputs, feed_dict={agent.input_layer: [state]})

            action_choice = np.random.choice(locations, p=action_probabilities[0])

            # Save the resulting states, rewards and whether the episode finished
            state_next, reward, done, _ = env.step(action_choice)

            episode_history.append([state, action_choice, reward, state_next])
            state = state_next

            episode_rewards += reward

            if done or step + 1 == max_steps_per_episode:
                total_episode_rewards.append(episode_rewards)
                episode_history = np.array(episode_history)

                # normalize rewards fn on the stored rewards in episode history
                episode_history[:, 2] = agent.discount_normalize_rewards(episode_history[:, 2])

                ep_gradients = sess.run(agent.gradients,
                                        feed_dict={agent.input_layer: np.vstack(episode_history[:, 0]),
                                                   agent.actions: episode_history[:, 1],
                                                   agent.rewards: episode_history[:, 2]})

                # add the gradients
                for index, gradient in enumerate(ep_gradients):
                    gradient_buffer[index] += gradient

                break
        if episode % episode_batch_size == 0:
            feed_dict_gradients = dict(zip(agent.gradients_to_apply, gradient_buffer))

            sess.run(agent.update_gradients, feed_dict=feed_dict_gradients)

            for index, gradient in enumerate(gradient_buffer):
                gradient_buffer[index] = gradient * 0

            if episode % 100 == 0:
                saver.save(sess, path + "pg-checkpoint", episode)

                print("Average reward / 100 eps: " + str(np.mean(total_episode_rewards[-100:])))

print("Now Testing neural network... \n")
testing_episodes = 2

with tf.Session() as sess:
    checkpoint = tf.train.get_checkpoint_state(path)
    saver.restore(sess, checkpoint.model_checkpoint_path)

    for episode in range(testing_episodes):

        state_all = env.reset()

        state = state_all[3]

        episode_rewards = 0

        for step in range(max_steps_per_episode):
            env.render("on")

            # Get Action
            action_argmax = sess.run(agent.choice, feed_dict={agent.input_layer: [state]})
            action_choice = action_argmax[0]

            state_next, reward, done, _ = env.step(action_choice)
            state = state_next

            episode_rewards += reward

            if done or step + 1 == max_steps_per_episode:
                print("Rewards for episode " + str(episode) + ": " + str(episode_rewards))
                break


