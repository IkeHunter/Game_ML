import numpy as np

import random

import game_library as gl
import game_main as gm

locations = gl.locations
pc = gl.possible_encounters


class Player:

    def __init__(self, name="Guest"):
        self.name = name
        self.health = 3
        self.moves = 0
        self.has_chest = False
        self.is_dead = False
        self.max_moves = 30

    def view_health(self):
        health = str(self.health)
        return health

    def view_health_num(self):
        return self.health

    def view_moves(self):
        moves = str(self.moves)
        return moves

    def view_moves_num(self):
        return self.moves

    def effect_health(self, amount):
        if amount < 0:
            if self.health - amount > 0:
                self.health += amount
                return self.health
            else:
                self.health = 0
                return self.health
        elif amount > 0:
            self.health += amount
            return self.health

    def effect_moves(self, amount):
        self.moves += amount
        return self.moves

    def obtains_chest(self):
        self.has_chest = True
        return self.has_chest

    def add_move(self):
        self.moves += 1
        return None


class Program:

    def __init__(self):
        self.player = Player("Machine")
        self.current_location = 0
        self.loop_break = False
        self.encountered = 0
        self.render = False
        self.reward = 0.0
        self.max_moves = self.player.max_moves
        self.has_chest = 0
        self.has_chest_bool = False
        self.has_won = False
        self.move_log = []

    def obtained_chest(self):
        if self.current_location == 12 and self.player.has_chest is False:
            text = "You have obtained the chest, hurry to the Coffee Shop! \n "
            self.render_text(text)
            self.player.obtains_chest()
            self.reward += 100.0
            self.has_chest = 1
            self.has_chest_bool = True

    def player_won(self):
        if (self.has_chest == 0) and (self.current_location == 11) and (self.player.view_health_num() > 0):
            text = "You Win! \n "
            self.render_text(text)
            self.reward += 500.0
            self.has_won = True
            self.loop_break = True

    def init_play(self):
        text = "Welcome {0.player.name}, the objective is to obtain a chest of gold and take it to " \
               "the Grand Master at the Coffee Shop".format(self)

        text += "\nYou must do so while trying to avoid goblins, they hide in different locations, " \
                "and constantly are on the move."

        text += "\nIf a goblin sees you, you lose a some health, with {0} healths to start with."\
            .format(self.player.view_health())

        text += "\nHowever, if a doctor happens to be at that location, you can gain a health."

        text += "\nGood luck!"

        self.render_text(text)

    def print_locs(self, action):
        text = self.locations_print()
        self.render_text(text)

        available_directions = self.user_direction(action)
        return available_directions

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

    def user_direction(self, action):
        if not self.render:
            player_option = action
        else:
            player_option = action
            text = "Directon: {}".format(player_option)
            self.render_text(text)

        player_option, available_directions = self.direction_query(player_option)

        if player_option is "Q":
            text = "Have a good day! \n \n"
            self.render_text(text)
            self.loop_break = True
        elif player_option is "X":
            self.reward -= 15.0
            self.player.add_move()
            return available_directions
        else:
            self.reward += 1.0
            self.current_location = self.advance_location(player_option)  # moves to next location
            self.player.add_move()
            return available_directions

    def direction_query(self, user_input):
        available_keys = []  # inclusive
        available_directions = []  # exclusive
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
            user_input = "X"

        return user_input, available_directions

    def advance_location(self, direction):
        global locations
        move_to = locations[self.current_location]["directions"][direction]
        return move_to

    def location_health(self):
        passed = True

        max_num = locations[self.current_location]["death"]

        health_bool = random_num(max_num)

        self.encountered = 0

        if health_bool is True:
            self.encountered = 1
            self.player.effect_health(-1)
            self.reward -= 2.0
            passed = False

        else:
            max_num = locations[self.current_location]["heal"]
            health_bool = random_num(max_num)
            if health_bool is True:
                self.encountered = 2
                self.player.effect_health(1)
                self.reward += 2.0

        if passed:
            self.reward += 1.0

        text = pc[self.encountered]

        return text

    def encountered_stats(self):
        things_encountered = self.location_health()
        health = self.player.view_health()
        moves = self.player.view_moves()
        rewards = int(self.reward)

        if health == "0":
            self.loop_break = True

        text = ("-" * 59)
        text += "\n| Encountered: {0}, Health: {1:2}, Moves: {2:2}, Rewards: {3:2} |\n".format(things_encountered, health, moves, rewards)
        text += ("-" * 59)
        text += " \n"

        self.render_text(text)
        return self.encountered, health, moves

    def check_instance(self):

        moves = self.player.view_moves_num()

        if moves >= self.max_moves:
            text = "Too many moves!"
            self.render_text(text)
            self.reward -= 10
            self.loop_break = True

        if self.player.health == 0:
            text = "You have no more life, you lose \n "
            self.render_text(text)
            self.reward -= 12
            self.loop_break = True

        return self.loop_break

    def render_text(self, text):

        self.move_log += text

        if self.render:
            print(text)


class GameMethods:

    def __init__(self):
        self.game = Program()

    def reset(self):
        self.game.player.health = 3
        self.game.player.moves = 0
        self.game.current_location = 0
        self.game.encountered = 0
        self.game.loop_break = False
        self.game.reward = 0.0
        self.game.has_chest = 0
        self.game.has_chest_bool = False
        self.game.has_won = False
        self.game.move_log = []

        observations = np.array([self.game.encountered, self.game.has_chest])

        return self.game.player.health, self.game.player.moves, self.game.current_location, observations

    def render(self, status):
        # current = self.game.current_location
        logs = self.game.move_log

        if status == "off":
            self.game.render = False
        elif status == "on":
            self.game.render = True

        # return current
        return logs

    def step(self, action):

        action = gl.directions[action]["short"]

        encountered, health, moves, available_directions = gm.machine_loop(action, self.game)

        token = self.game.max_moves - int(moves)
        self.game.reward += token

        obs = np.array([encountered, self.game.has_chest])
        reward = np.array([self.game.reward])
        done = self.game.loop_break
        won = self.game.has_won
        chest = self.game.has_chest
        info = dict()

        return obs, reward, done, info

    def has_won(self):
        return self.game.has_won, self.game.has_chest_bool

    def close(self):
        self.game.loop_break = True


class User:

    def __init__(self):
        self.player = Player()
        self.current_location = 0
        self.loop_break = False
        self.reward = 0
        self.max_moves = self.player.max_moves

    def main(self):
        pass

    def init_play(self):
        name = input("\nPlease enter your name: ")
        self.player = Player(name)

        self.intro()

    def intro(self):
        print(
            "\nWelcome {0.player.name}, the objective is to obtain a chest of gold and take it "
            "to the Grand Master at the Coffee Shop".format(self))
        print("You must do so while trying to avoid goblins, they hide in different locations, "
              "and constantly are on the move.")
        print("If a goblin sees you, you lose a some health, with {0} healths to start with.".format(
            self.player.view_health()))
        print("However, if a doctor happens to be at that location, you can gain a health.")
        print("Good luck!\n")

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
            self.player.add_move()

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
                self.reward -= 15
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
        else:
            self.reward += 1

        return user_input

    def advance_location(self, direction):
        global locations
        move_to = locations[self.current_location]["directions"][direction]
        return move_to

    def location_health(self):
        passed = True
        max_num = locations[self.current_location]["death"]

        health_bool = random_num(max_num)
        text = "Nobody"
        if health_bool is True:
            text = "Goblin"
            self.player.effect_health(-1)
            self.reward -= 2
            passed = False

        else:
            max_num = locations[self.current_location]["heal"]
            health_bool = random_num(max_num)
            if health_bool is True:
                text = "Doctor"
                self.player.effect_health(1)
                self.reward += 2

        if passed:
            self.reward += 1

        return text

    def encountered_stats(self):
        did_encounter = self.location_health()
        health = self.player.view_health()
        moves = self.player.view_moves()
        rewards = self.reward

        if health == "0":
            self.loop_break = True

        text = ("-" * 59)
        text += "\n| Encountered: {0}, Health: {1:2}, Moves: {2:2}, Rewards: {3:2} |\n"\
            .format(did_encounter, health, moves, rewards)
        text += ("-" * 59)
        print(text)
        print()


def random_num(max_range):
    num = random.randint(0, 10)
    num_list = []
    for i in range(0, max_range):
        num_list.append(i)
    if num in num_list:
        return True  # If the odds are right, it returns True (player loses/gains health)
    else:
        return False  # If they are wrong, it returns False (nothing happens to player)
