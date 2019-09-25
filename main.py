import arcade
from Game import Game
import os
import sys
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NEAT ALGORITHM FOR A 2D PLATTFORM GAME" 

def main():

	#Path to NEAT config file
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config')

	#Initalize and start game
	game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	game.setup_neat("D:\Programmering\TNM095-Project\config")
	game.setup()
	game.run()


if __name__ == "__main__":
	main()
