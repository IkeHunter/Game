import game_classes as gc
import agent_main as am


def main():
    decision = input("Play [0] machine, or [1] player?: ")

    if decision == "0":
        return am.neural_network_loop()
    elif decision == "1":
        return player_loop()
    else:
        print("Decision not valid")


def machine_loop(action, game):

    game.obtained_chest()

    game.player_won()

    available_directions = game.print_locs(action)

    encountered, health, moves = game.encountered_stats()

    game.check_instance()

    return encountered, health, moves, available_directions


def player_loop():
    program = gc.User()

    program.init_play()

    while True:

        if program.current_location == 12 and program.player.has_chest is False:
            print("You have obtained the chest, hurry to the Coffee Shop!")
            print()
            program.player.obtains_chest()
            program.reward += 100

        if (program.player.has_chest is True) and (program.current_location is 11) and (program.player.view_health() is not 0):
            print("You win!")
            print()
            program.reward += 500
            break

        if program.player.view_moves_num() > program.max_moves:
            print("Too many moves!")
            print()
            program.reward -= 10
            break

        if program.loop_break:
            print("You have no more life, you lose")
            print()
            program.reward -= 12
            break

        program.print_locs()

        if program.loop_break:
            break

        program.encountered_stats()


if __name__ == '__main__':
    main()
