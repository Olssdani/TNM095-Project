'''
Main file for initialize the game and running it
'''

import arcade
from Game import Game
import os
import sys
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NEAT ALGORITHM FOR A 2D PLATTFORM GAME" 

def main():

	#Get path to neat file .
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(os.path.dirname(__file__), 'config')


	print("To run new run type 'n', to continue on a saved run type 'c' and to run best genome from one saved run type 'b'")
	choice_of_run = input();
	
	#Initalize and start game
	game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	game.setup_neat(config_path,choice_of_run )
	game.setup()
	game.run()


if __name__ == "__main__":
	main()
