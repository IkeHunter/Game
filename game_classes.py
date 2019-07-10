import random

import game_library as gl

locations = gl.locations


class Player:

    def __init__(self, name="Guest"):
        self.name = name
        self._health = 3
        self._moves = 0
        self.has_chest = False
        self.is_dead = False

    def view_health(self):
        health = str(self._health)
        return health

    def view_health_num(self):
        return self._health

    def view_moves(self):
        moves = str(self._moves)
        return moves

    def effect_health(self, amount):
        if amount < 0:
            if self._health - amount > 0:
                self._health += amount
                return self._health
            else:
                self._health = 0
                return self._health
        elif amount > 0:
            self._health += amount
            return self._health

    def effect_moves(self, amount):
        self._moves += amount
        return self._moves

    def obtains_chest(self):
        self.has_chest = True
        return self.has_chest

    def add_move(self):
        self._moves += 1
        return None


class Program:

    def __init__(self):
        self.player = None
        self.current_location = 0
        self.loop_break = False

    def main(self):
        pass

    def init_play(self):
        name = "Machine"
        self.player = Player(name)

        self.intro()

    def intro(self):
        print(
            "Welcome {0.player.name}, the objective is to obtain a chest of gold and take it "
            "to the Grand Master at the Coffee Shop".format(self))
        print("You must do so while trying to avoid goblins, they hide in different locations, "
              "and constantly are on the move.")
        print("If a goblin sees you, you lose a some health, with {0} healths to start with.".format(
            self.player.view_health()))
        print("However, if a doctor happens to be at that location, you can gain a health.")
        print("Good luck!")

    def print_locs(self):
        # print(self.locations_print
        text = self.locations_print()
        print(text)

        self.user_direction()

    def locations_print(self):
        global locations
        location = locations[self.current_location]["name"]

        text = "You are currently next to a {0}, you can go ".format(location)
        for i in range(0, len(locations[self.current_location]["locations"])):
            if locations[self.current_location]["locations"][i] is not "Q":
                if (i + 2) < (len(locations[self.current_location]["locations"])):
                    text += str(locations[self.current_location]["locations"][i]) + ", "
                elif (i + 2) == (len(locations[self.current_location]["locations"])):
                    text += str(locations[self.current_location]["locations"][i])

        return text

    def user_direction(self):
        player_option = input("Direction: ").upper()
        player_option = self.direction_query(player_option)

        if player_option is "Q":
            print("Have a good day!")
            print()
            self.loop_break = True

        else:
            self.current_location = self.advance_location(player_option)  # moves to next location

    def direction_query(self, user_input):
        available_keys = []
        available_directions = []
        problems = False

        for i in gl.directions.values():
            available_keys.append(i["short"])
            available_keys.append(i["long"])

        for i in gl.locations[self.current_location]["locations"]:
            available_directions.append(i)

        if user_input in available_keys:
            for i in range(0, len(gl.directions)):
                if user_input in gl.directions[i].values():
                    user_input = gl.directions[i]["short"]
                    break

        if user_input not in available_keys:
            problems = True

        if (user_input in available_keys) and (user_input not in available_directions):
            problems = True

        if problems is True:
            while problems is True:
                user_input = input("Please enter a valid direction: ").upper()
                if user_input in available_keys:
                    for i in range(0, len(gl.directions)):
                        if user_input in gl.directions[i].values():
                            user_input = gl.directions[i]["short"]
                            break
                    problems = False
                    if user_input in available_directions:
                        problems = False
                    else:
                        problems = True
                else:
                    problems = True

        return user_input

    def advance_location(self, direction):
        global locations
        move_to = locations[self.current_location]["directions"][direction]
        return move_to

    def location_health(self):
        max_num = locations[self.current_location]["death"]

        health_bool = random_num(max_num)
        text = "Nobody"
        if health_bool is True:
            text = "Goblin"
            self.player.effect_health(-1)

        else:
            max_num = locations[self.current_location]["heal"]
            health_bool = random_num(max_num)
            if health_bool is True:
                text = "Doctor"
                self.player.effect_health(1)

        return text

    def encountered_stats(self):
        did_encounter = self.location_health()
        health = self.player.view_health()
        moves = self.player.view_moves()

        if health == "0":
            self.loop_break = True

        print()
        print('-' * 46)
        print("| Encountered: {0}, Health: {1:2}, Moves: {2:2} |"
              .format(did_encounter, health, moves))
        print('-' * 46)


def random_num(max_range):
    num = random.randint(0, 10)
    num_list = []
    for i in range(0, max_range):
        num_list.append(i)
    if num in num_list:
        return True  # If the odds are right, it returns True (player loses/gains health)
    else:
        return False  # If they are wrong, it returns False (nothing happens to player)
