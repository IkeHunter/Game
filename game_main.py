import game_classes as gc

player = gc.Player()
program = gc.Program()


def main(action, game):

    # if program.current_location == 12:
    #     text = "You have obtained the chest, hurry to the Coffee Shop! \n "
    #     program.render_text(text)
    #     player.obtains_chest()

    game.obtained_chest()

    if (game.player.has_chest is True) and (game.current_location is 11) and (game.player.view_health() is not 0):
        text = "You Win! \n "
        game.render_text(text)
        game.reward.append(1.0)
        game.break_loop = True

    if game.loop_break:
        text = "You have no more life, you lose \n "
        game.render_text(text)
        game.break_loop = True

    available_directions = game.print_locs(action)

    encountered, health, moves = game.encountered_stats()

    return encountered, health, moves, available_directions


def main_looped():

    program.init_play()

    while True:

        if program.current_location == 12:
            text = "You have obtained the chest, hurry to the Coffee Shop! \n "
            program.render_text(text)
            player.obtains_chest()

        if (player.has_chest is True) and (program.current_location is 11) and (player.view_health() is not 0):
            text = "You Win! \n "
            program.render_text(text)
            break

        if program.loop_break:
            text = "You have no more life, you lose \n "
            program.render_text(text)
            break

        program.print_locs()

        if program.loop_break:
            break

        program.encountered_stats()


if __name__ == '__main__':
    main_looped()
