import tensorflow as tf
import numpy as np


class Agent:

    def __init__(self, num_actions, state_size):
        self.num_actions = num_actions
        self.discount_rate = 0.95

        initializer = tf.contrib.layers.xavier_initializer()  # initializes some starting values for the neurons

        # this will let someone pass any number of states into the network in a batch
        self.input_layer = tf.placeholder(dtype=tf.float32, shape=[None, state_size])

        # Neural net starts here...

        # creates a hidden layer connected to input layer with 8 units, relu activation, and the xavier initializer
        hidden_layer_1 = tf.layers.dense(self.input_layer, 8, activation=tf.nn.relu, kernel_initializer=initializer)
        hidden_layer_2 = tf.layers.dense(hidden_layer_1, 8, activation=tf.nn.relu, kernel_initializer=initializer)

        # Output of neural net...

        out = tf.layers.dense(hidden_layer_2, self.num_actions, activation=None)  # num_actions must be int

        self.outputs = tf.nn.softmax(out)
        self.choice = tf.argmax(self.outputs, axis=1)  # ' axis=1 ' indicates maximum value of axis 1(action weights) is wanted

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

        optimizer = tf.train.AdamOptimizer(learning_rate=1e-2)
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

    def set_action_num(self, num):
        self.num_actions = num
        return self.num_actions
