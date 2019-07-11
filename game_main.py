import game_classes as gc

player = gc.Player()
program = gc.Program()


def main(action):

    # if program.current_location == 12:
    #     text = "You have obtained the chest, hurry to the Coffee Shop! \n "
    #     program.render_text(text)
    #     player.obtains_chest()

    program.obtained_chest()

    if (player.has_chest is True) and (program.current_location is 11) and (player.view_health() is not 0):
        text = "You Win! \n "
        program.render_text(text)
        program.reward.append(1.0)
        program.break_loop = True

    if program.loop_break:
        text = "You have no more life, you lose \n "
        program.render_text(text)
        program.break_loop = True

    available_directions = program.print_locs()

    encountered, health, moves = program.encountered_stats()

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
