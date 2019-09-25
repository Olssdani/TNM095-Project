import arcade
from datetime import time
import neat
from neat.reporting import ReporterSet
from neat.math_util import mean
from neat.six_util import iteritems, itervalues
from arcade.arcade_types import Point
import numpy as np

import gc
#Scaling of sprites
TILE_SCALING = 0.5
CHARACTER_SCALING = 0.4
ENEMY_SCALING = 0.5

#Player Constants!
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1
PLAYER_JUMP_SPEED = 18
ACCELERATION = 40

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100
START_POSITION_X = 200
INPUT_GRID_SIZE = 7 #Keep uneven!!!


class Game(arcade.Window):
	#Constructor 
	def __init__(self, width, height, title):
		
		#Initalize parent object with is the arcade.window
		super().__init__(width, height, title, resizable=True)
		
		'''
		Initlization of member variables
		'''
		#Sprite lists
		self.plattform_list = None
		self.player_list = None
		self.death_list = None
		self.end_list = None
		self.enemy_list = None
		self.player = None
		self.background_list = None

		#Screen variables
		self.Screen_Width = width
		self.Screen_Height = height
		
		#Input controls variables
		self.right_button_pressed = False
		self.left_button_pressed = False
		self.jump_button_pressed = False
		self.speed_x = 0
		
		#Game specific variables
		self.game_over = False
		self.score_distance = 0

		#Neat
		self.config_neat = None
		self.p = None
		self.gnomes = None
		self.current_genome_index = 0
		self.current_genome = None
		self.input_tiles = None
		self.last_position_x = 0
		self.last_position_y = 0
		self.tile_step = INPUT_GRID_SIZE//2
		self.net = None
		self.counter = 0

		
	def setup_neat(self, config_file): 
		self.config_neat = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

		self.p = neat.Population(self.config_neat)	

		self.genomes = list(iteritems(self. p.population))

		self.input_tiles = [[0 for x in range(INPUT_GRID_SIZE)] for y in range(INPUT_GRID_SIZE)]


	#TODO Implement the code to evolve the genomes
	def evolve_genomes(self):
		print("Evovle")
		

	#Game setup, Initliaze and load variables.
	def setup(self):
		#Setup the sprite lists
		self.plattform_list = arcade.SpriteList()
		self.player_list = arcade.SpriteList()
		self.death_list = arcade.SpriteList()
		self.end_list = arcade.SpriteList()
		self.enemy_list = arcade.SpriteList()
		self.background_list = arcade.SpriteList()

		#Initalize the player sprite and vairables
		self.player = arcade.Sprite("Sprites/Used/Player.png", CHARACTER_SCALING)
		self.player.center_y = 200
		self.player.center_x = START_POSITION_X
		self.player_list.append(self.player)
		self.score_distance = 0
		self.speed_x = 0

		# --- Load in a map from the tiled editor ---
		# Name of map file to load
		map_name = "Easy.tmx"
		
		# Names of the layers
		platforms_layer_name = 'Plattform'
		death_layer_name = 'Death'
		end_layer_name = 'End'
		enemy_layer_name = 'Enemy'
		plattform_layer_name = 'Background'

		# Read in the tiled map
		my_map = arcade.tilemap.read_tmx(map_name)

		# Read the tilemaps
		self.plattform_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
		self.death_list = arcade.tilemap.process_layer(my_map, death_layer_name, TILE_SCALING)
		self.end_list = arcade.tilemap.process_layer(my_map, end_layer_name, TILE_SCALING)
		self.enemy_list = arcade.tilemap.process_layer(my_map, enemy_layer_name, ENEMY_SCALING)
		self.background_list = arcade.tilemap.process_layer(my_map, plattform_layer_name, TILE_SCALING)
		#Set the movement for the enemies
		for enemy in self.enemy_list:
			enemy.change_x = 2

		# Set the background color
		if my_map.background_color:	
			arcade.set_background_color(my_map.background_color)

		# Create the 'physics engine'
		self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.plattform_list, GRAVITY)
		
		#Used to keep track of our scrolling
		self.view_bottom = 0
		self.view_left = 0

		#Neat
		if(self.current_genome_index > len(self.genomes) - 1):
			self.evolve_genomes()
			self.current_genome_index = 0

		self.current_genome = self.genomes[self.current_genome_index][1]

		self.net = neat.nn.recurrent.RecurrentNetwork.create(self.current_genome, self.config_neat)

	#Draw all sprites during rendering
	def on_draw(self):
		#Start the rendering
		arcade.start_render()
		
		#Draw the objects
		self.plattform_list.draw()
		self.player_list.draw()
		self.death_list.draw()
		self.end_list.draw()
		self.enemy_list.draw()
		self.background_list.draw()
		

		# Draw our score on the screen, scrolling it with the viewport
		score_text = f"Score: {self.score_distance}"
		arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)


	#Resize the window if user wants
	def on_resize(self, width, height):
		super().on_resize(width, height)
		self.Screen_Width = width
		self.Screen_Height = height


	#Print the input tiles in the console, used for debug
	def print_input_tile(self):
		#Print tile, for debug use only
		for y in range(INPUT_GRID_SIZE):
			for x in range(INPUT_GRID_SIZE):
				if(x == INPUT_GRID_SIZE-1):
					print(self.input_tiles[y][x])
				else:
					print(self.input_tiles[y][x], end=' ')


		print(" ")


	#Return value for the tile depending on whats on that tile
	def get_tile_sort(self, point):
		#Value for the tiles is hostile =-1, nothing = 0 and plattform =1
		#Plattform
		if len(arcade.get_sprites_at_point(point, self.plattform_list)) > 0:
			return 1
		#Enemy
		elif len(arcade.get_sprites_at_point(point, self.enemy_list)) > 0:
			return -1
		#Rest
		else:
			return 0
	

	#Get tiles in a souranding area around the player as input.
	def get_input_tiles(self):
		#Get the tile position that the player are on
		player_x = (self.player.center_x // 64 ) * 64 + 32
		player_y = (self.player.center_y // 64 ) * 64 + 32
		
		#Check if player have moved into another tile
		if(self.last_position_y !=player_y or self.last_position_x != player_x):
			#print("Last: " +str(self.last_position_x) + " New: " + str(player_x))
			#If player has moved into another square in both directions 
			
			if(self.last_position_y !=player_y and self.last_position_x != player_x):
				for y in range(INPUT_GRID_SIZE):
					for x in range(INPUT_GRID_SIZE):
						point  = (player_x+(x-self.tile_step)*64, player_y-(y-self.tile_step)*64)
						self.input_tiles[y][x] = self.get_tile_sort(point)			
			
			elif (self.last_position_x < player_x):

				for y in range(INPUT_GRID_SIZE):
					for x in range(1,INPUT_GRID_SIZE):
						self.input_tiles[y][x-1] = self.input_tiles[y][x]
				for y in range(INPUT_GRID_SIZE):
					point  = (player_x+(self.tile_step)*64, player_y-(y-self.tile_step)*64)
					self.input_tiles[y][INPUT_GRID_SIZE-1] = self.get_tile_sort(point)
			
			elif (self.last_position_x > player_x):
				for y in range(INPUT_GRID_SIZE):
					for x in range(INPUT_GRID_SIZE-2, -1, -1):
						self.input_tiles[y][x+1] = self.input_tiles[y][x]
				for y in range(INPUT_GRID_SIZE):
					point  = (player_x-(self.tile_step)*64, player_y-(y-self.tile_step)*64)
					self.input_tiles[y][0] = self.get_tile_sort(point)
			
			
			elif (self.last_position_y < player_y):
				
				for x in range(INPUT_GRID_SIZE):
					for y in range(INPUT_GRID_SIZE-2, -1, -1):
						self.input_tiles[y+1][x] = self.input_tiles[y][x]
				for x in range(INPUT_GRID_SIZE):
					point  = (player_x-(x-self.tile_step)*64, player_y+(self.tile_step)*64)
					self.input_tiles[0][x] = self.get_tile_sort(point)
			elif (self.last_position_y > player_y):		
				for x in range(INPUT_GRID_SIZE):
					for y in range(INPUT_GRID_SIZE-1):
						self.input_tiles[y][x] = self.input_tiles[y + 1][x]
				for x in range(INPUT_GRID_SIZE):
					point  = (player_x + (x - self.tile_step) * 64, player_y - self.tile_step * 64)
					self.input_tiles[INPUT_GRID_SIZE-1][x] = self.get_tile_sort(point)
				
			#self.print_input_tile()
		#Update last postion
		self.last_position_x = player_x
		self.last_position_y = player_y
	

	#Oncall method on key press, sets specific variable to true and the movement is handle elsewhere
	def on_key_press(self, key, modifiers):
		"""Called whenever a key is pressed. """
		if key == arcade.key.UP or key == arcade.key.W:
			self.jump_button_pressed = True
		if key == arcade.key.LEFT or key == arcade.key.A:
			self.left_button_pressed = True
			self.player.change_x = -PLAYER_MOVEMENT_SPEED
		if key == arcade.key.RIGHT or key == arcade.key.D:
			self.right_button_pressed = True
			self.player.change_x = PLAYER_MOVEMENT_SPEED


	#Oncall method for key realese, change the specific variable
	def on_key_release(self, key, modifiers):
		"""Called when the user releases a key. """
		if key == arcade.key.UP or key == arcade.key.W:
			self.jump_button_pressed = False
		if key == arcade.key.LEFT or key == arcade.key.A:
			self.left_button_pressed = False
		elif key == arcade.key.RIGHT or key == arcade.key.D:
			self.right_button_pressed = False


	#Function to update movement speed to include accerelation and deaccerelation
	def update_movement(self, delta_time):
		#Jump
		if self.jump_button_pressed:
			if self.physics_engine.can_jump():
				self.player.change_y = PLAYER_JUMP_SPEED

		#Left button pressed accerelation
		if self.left_button_pressed and not self.right_button_pressed:
			self.speed_x -= ACCELERATION * delta_time

			#Check if speed is larger than max speed
			if(self.speed_x < -PLAYER_MOVEMENT_SPEED):
				self.speed_x = -PLAYER_MOVEMENT_SPEED
		
		#Left button released deaccerelation
		elif self.speed_x < 0 and not self.right_button_pressed:
			self.speed_x += ACCELERATION * delta_time
			
			#Check for min speed
			if(self.speed_x > 0):
				self.speed_x = 0
		
		#Right button pressed accerelation
		if self.right_button_pressed and not self.left_button_pressed:
			self.speed_x += ACCELERATION * delta_time

			#Check for max speed
			if(self.speed_x > PLAYER_MOVEMENT_SPEED):
				self.speed_x = PLAYER_MOVEMENT_SPEED
		
		#Right button released and deaccerelation
		elif self.speed_x > 0 and not self.left_button_pressed:
			self.speed_x -= ACCELERATION * delta_time
			
			#Check for min speed
			if(self.speed_x < 0):
				self.speed_x = 0
		
		#Add the change to the sprite
		self.player.change_x = self.speed_x 


	#Update the score depending on the distance
	def update_score(self):
	 	new_score =int((self.player.center_x-START_POSITION_X) / 64)
	 	
	 	#Make sure that the score does not decrease if going backwards
	 	if new_score>self.score_distance:
	 		self.score_distance = new_score
	 		self.counter = 0
	 	else:
	 		self.counter +=1 
		

	#Managing the scrolling of the screen
	def scrolling(self):
		# Track if we need to change the viewport
		changed = False

		# Scroll left
		left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN	
		if self.player.left < left_boundary:
			self.view_left -= left_boundary - self.player.left
			changed = True

		# Scroll right
		right_boundary = self.view_left + self.Screen_Width - RIGHT_VIEWPORT_MARGIN
		if self.player.right > right_boundary:
			self.view_left += self.player.right - right_boundary
			changed = True

		# Scroll up
		top_boundary = self.view_bottom + self.Screen_Height - TOP_VIEWPORT_MARGIN
		if self.player.top > top_boundary:
			self.view_bottom += self.player.top - top_boundary
			changed = True

		# Scroll down
		bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
		if self.player.bottom < bottom_boundary and self.player.bottom>BOTTOM_VIEWPORT_MARGIN:
			self.view_bottom -= bottom_boundary - self.player.bottom
			changed = True

		if changed:
			# Only scroll to integers. Otherwise we end up with pixels that
			# don't line up on the screen
			self.view_bottom = int(self.view_bottom)
			self.view_left = int(self.view_left)

			# Do the Scrolling
			arcade.set_viewport(self.view_left, self.Screen_Width + self.view_left, self.view_bottom, self.Screen_Height + self.view_bottom)


	#Update all sprites		
	def update(self, delta_time):
		#Variable definition
		should_end = False
		inputs = list(())
		self.get_input_tiles()
		for y in range(INPUT_GRID_SIZE):
			for x in range(INPUT_GRID_SIZE):
				inputs.append(self.input_tiles[y][x])
	
		
		nnOutput = self.net.activate(inputs)
		#print(nnOutput)
		nnOutput[0] = round(nnOutput[0])
		nnOutput[1] = round(nnOutput[1])
		nnOutput[2] = round(nnOutput[2])
		print(nnOutput)
		self.left_button_pressed = nnOutput[0]
		self.jump_button_pressed = nnOutput[1]
		self.right_button_pressed = nnOutput[2]
		#Update the movement on the player
		self.update_movement(delta_time)

		 # Update the player based on the physics engine and move the enemies
		if not self.game_over:
			
			# Move the enemies
			self.enemy_list.update()

			# Check each enemy
			for enemy in self.enemy_list:
				# If the enemy hit a wall, reverse
				if len(arcade.check_for_collision_with_list(enemy, self.plattform_list)) > 0:
					enemy.change_x *= -1
			
			# Update the player using the physics engine
			self.physics_engine.update()

			# See if the player hit a enemy, just restart 
			'''
			TODO STORE SCORE FOR EVALUATING
			'''
			if len(arcade.check_for_collision_with_list(self.player, self.enemy_list)) > 0:
				should_end = True
			if arcade.check_for_collision_with_list(self.player, self.death_list):
				should_end = True
			if arcade.check_for_collision_with_list(self.player, self.end_list):
				should_end = True

		self.scrolling()
		self.update_score()

		if self.counter > 200:
			self.counter = 0
			should_end = True
		if should_end:
			self.genomes[self.current_genome_index][1].fitness = self.score_distance
			self.current_genome_index +=1
			print("On genome number: " + str(self.current_genome_index))
			self.setup()
			


	def run(self):
		arcade.run()
		