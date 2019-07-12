import tensorflow as tf
import numpy as np
import game_library as gl
import game_classes as gc
import random


class Agent:

    def __init__(self, num_actions, state_size):
        self.num_actions = num_actions
        self.discount_rate = 0.95
        self.env = gc.GameMethods()

        initializer = tf.contrib.layers.xavier_initializer()  # initializes some starting values for the neurons

        # this will let someone pass any number of states into the network in a batch
        self.input_layer = tf.placeholder(dtype=tf.float32, shape=[None, state_size])

        # Neural net starts here...

        # creates a hidden layer connected to input layer with 8 units, relu activation, and the xavier initializer
        # hidden_layer_1 = tf.layers.dense(self.input_layer, 2, activation=tf.nn.relu, kernel_initializer=initializer)
        # hidden_layer_2 = tf.layers.dense(hidden_layer_1, 2, activation=tf.nn.relu, kernel_initializer=initializer)

        conv_layer_1 = tf.layers.conv1d(self.input_layer, filters=32, kernel_size=3, padding="same", activation=tf.nn.relu)
        pooling_layer_1 = tf.layers.max_pooling1d(conv_layer_1, pool_size=3, strides=1)

        conv_layer_2 = tf.layers.conv1d(pooling_layer_1, filters=32, kernel_size=2, padding="same", activation=tf.nn.relu)
        pooling_layer_2 = tf.layers.max_pooling1d(conv_layer_2, pool_size=2, strides=2)

        conv_layer_3 = tf.layers.conv1d(pooling_layer_2, filters=32, kernel_size=2, padding="same", activation=tf.nn.relu)
        pooling_layer_3 = tf.layers.max_pooling1d(conv_layer_3, pool_size=2, strides=2)

        flattened_pooling = tf.layers.flatten(pooling_layer_3)
        dense_layer = tf.layers.dense(flattened_pooling, 1024, activation=tf.nn.relu)

        # Output of neural net...

        out = tf.layers.dense(dense_layer, self.num_actions, activation=None)  # num_actions must be int

        self.outputs = tf.nn.softmax(out)
        self.choice = tf.argmax(self.outputs, axis=1)
        # ' axis=1 ' indicates maximum value of axis 1(action weights) is wanted

        self.rewards = tf.placeholder(shape=[None, ], dtype=tf.float32)
        self.actions = tf.placeholder(shape=[None, ], dtype=tf.int32)

        one_hot_actions = tf.one_hot(self.actions, self.num_actions)

        cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=out, labels=one_hot_actions)

        self.loss = tf.reduce_mean(cross_entropy * self.rewards)

        self.gradients = tf.gradients(self.loss, tf.trainable_variables())

        # Create a placeholder list for gradients
        self.gradients_to_apply = []
        for index, variable in enumerate(tf.trainable_variables()):
            gradient_placeholder = tf.placeholder(tf.float32)
            self.gradients_to_apply.append(gradient_placeholder)

        # Create the operation to update gradients with the gradients placeholder...

        optimizer = tf.train.AdamOptimizer(learning_rate=1e-3)
        # Update gradients operation applies gradients that were fed into the corresponding trainable vars in the model
        # Operation runs every time model needs to appy what it has learned from its games and update its parameters
        self.update_gradients = optimizer.apply_gradients(zip(self.gradients_to_apply, tf.trainable_variables()))

    def discount_normalize_rewards(self, rewards):

        self.discounted_rewards = np.zeros_like(rewards)
        total_rewards = 0

        for i in reversed(range(len(rewards))):
            total_rewards = total_rewards * self.discount_rate + rewards[i]
            self.discounted_rewards[i] = total_rewards

        # Normalize rewards across multiple game lengths
        self.discounted_rewards -= np.mean(self.discounted_rewards)
        self.discounted_rewards /= np.std(self.discounted_rewards)

        return self.discounted_rewards

    def random_agent(self):
        games_to_play = 10

        for i in range(games_to_play):
            # Reset the env
            pack = self.env.reset()  # initialize all vars and prep game to run
            episode_rewards = 0
            done = False

            current = int(pack[2])
            locations = []
            for j in gl.locations[current]["direction_values"]:
                locations.append(j)
            action = random.choice(locations)

            while not done:
                pack = self.env.render("on")  # draws frame of the game

                current = pack
                locations = []
                for j in gl.locations[current]["direction_values"]:
                    locations.append(j)
                action = random.choice(locations)

                # Take a step in the env with the chosen action
                obs, reward, done, info = self.env.step(action)
                episode_rewards += reward
                # time.sleep(5)

            print("Total episode rewards: {} \n".format(str(episode_rewards)))  # print total rewards when done
            print("=" * 40)




