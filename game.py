from src.main import Game

game = Game()


while game.running:
    game.curr_menu.display_menu()
    while game.playing:
        game.gameplay()



   # game.game_loop()

# def main():
#     print("Starting the game")
#     game = Game()
#     game.curr_menu.display_menu()
#     #game.gameplay()
#     print("Game Over")


# main()
 