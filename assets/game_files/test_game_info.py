import assets.game_files.game_info as gi
game = gi.Game(0)
game.get_planes(0, "31d25l64u")
print(game.play(1, (3, 1)))
print(game.play(1, (2, 5)))
print(game.play(1, (6, 5)))
print(game.get_winner())
i = 1
def fct1():
    i = 0
    def print_fct(txt):
        global i
        print(txt + str(i))
        i += 1

    print_fct("da")
    print_fct("nu")
    print_fct("poate")
fct1()
