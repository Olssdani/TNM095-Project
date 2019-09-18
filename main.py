import arcade
from Game import Game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NEAT ALGORITHM FOR A 2D PLATTFORM GAME"


def main():
    print("Main")
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()
    arcade.close_window()


if __name__ == "__main__":
    main()
