from src.main import Game

game = Game()


while game.running:
    game.curr_menu.display_menu()
    print(game.playing)
    if game.playing:
        game.gameplay()


