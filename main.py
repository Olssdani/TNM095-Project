import arcade
from Game import Game
import os
import sys
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NEAT ALGORITHM FOR A 2D PLATTFORM GAME" 

def main():
	#Game creation and setup
	#game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	#game.setup()
	#Neat
	#ocal_dir = os.path.dirname(__file__)
	#config_path = os.path.join(local_dir, 'config')
	#game.setup_neat(config_path)
	
	#Start rendering
	stop = False
	#while not stop:

	game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	game.setup()
	game.run()
'''
	game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	game.setup()

	game.run()
	print("Here")
	print("Returned")
	
	del game1
'''

if __name__ == "__main__":
	main()
