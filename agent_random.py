import random

import game_library as gl


def random_agent(env):
    games_to_play = 10

    for i in range(games_to_play):
        # Reset the env
        pack = env.reset()  # initialize all vars and prep game to run
        episode_rewards = 0
        done = False

        # print("obs: {}, obs[2]: {}".format(pack, pack[2]))
        current = int(pack[2])
        locations = []
        for j in gl.locations[current]["locations"]:
            if j is not "Q":
                locations.append(j)
        action = random.choice(locations)

        while not done:
            pack = env.render("on")  # draws frame of the game

            current = pack
            locations = []
            for j in gl.locations[current]["locations"]:
                if j is not "Q":
                    locations.append(j)
            action = random.choice(locations)

            # Take a step in the env with the chosen action
            obs, reward, done, info = env.step(action)
            episode_rewards += reward
            # time.sleep(5)

        print("Total episode rewards: " + str(episode_rewards))  # print total rewards when done
