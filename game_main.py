import game_classes as gc


def main():
    player = gc.Player()
    program = gc.Program()

    program.init_play()

    while True:

        if (player.has_chest is True) and (program.current_location is 11) and (player.view_health() is not 0):
            print("You win!")
            print()
            break

        if player.view_health() == 0:
            print("You have no more life, you lose")
            print()
            break

        program.print_locs()

        if program.loop_break is True:
            break

        player.add_move()

        program.encountered_stats()


if __name__ == '__main__':
    main()
