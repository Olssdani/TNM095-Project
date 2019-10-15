'''
This file has the functionality to get the inputs around 
'''
from enum import Enum
import arcade


class Type(Enum):
	Plattform = 1
	Enemy = -1
	Nothing = 0


class Input():
	#Constructor 
	def __init__(self, grid_size):
		self.grid_size = grid_size


	#Return value for the tile depending on whats on that tile
	def get_tile_sort(self, point):
		#Value for the tiles is hostile =-1, nothing = 0 and plattform =1
		if len(arcade.get_sprites_at_point(point, self.plattform_list)) > 0:
			return 1
		else:
			return 0

	#Get tiles in a surrounding area around the player as input. Each tile corresponds to
	#a number where platfrom = 1, nothing = 0 and enemy = -1. Number of tiles is controlled
	#by the constant variable INPUT_GRID_SIZE
	def get_input_tiles(self):
		#Get the tile position that the player is on. The player position is clamp to an int and
		#is offset to half a tile size to get it to the center position
		player_x = (self.player.center_x // 64 ) * 64 + 32
		player_y = (self.player.center_y // 64 ) * 64 + 32
		
		for y in range(INPUT_GRID_SIZE):
			for x in range(INPUT_GRID_SIZE):
				point  = (player_x+(x-self.tile_step)*64, player_y-(y-self.tile_step)*64)
				if(len(arcade.get_sprites_at_point(point, self.enemy_list)) > 0):
					self.input_tiles[y][x] = -1
				elif(self.input_tiles[y][x] < 0):
					self.input_tiles[y][x] = 0
		#Check if player have moved into another tile otherwise do not update the input tiles
		if(self.last_position_y !=player_y or self.last_position_x != player_x):
			
			#If player has moved into another square in both directions, update the whole tile set
			#TODO optimize this by push the current tiles and just update the outer tiles	
			if(self.last_position_y !=player_y and self.last_position_x != player_x):
				for y in range(INPUT_GRID_SIZE):
					for x in range(INPUT_GRID_SIZE):
						point  = (player_x+(x-self.tile_step)*64, player_y-(y-self.tile_step)*64)
						self.input_tiles[y][x] = self.get_tile_sort(point)			
			
			#If the player has moved to the right
			elif (self.last_position_x < player_x):
				#Push the input tiles so only the outer tiles need to update
				for y in range(INPUT_GRID_SIZE):
					for x in range(1,INPUT_GRID_SIZE):
						self.input_tiles[y][x-1] = self.input_tiles[y][x]
				#Update the outer tiles
				for y in range(INPUT_GRID_SIZE):
					point  = (player_x+(self.tile_step)*64, player_y-(y-self.tile_step)*64)
					self.input_tiles[y][INPUT_GRID_SIZE-1] = self.get_tile_sort(point)
			
			#If the player has moved to the left
			elif (self.last_position_x > player_x):
				for y in range(INPUT_GRID_SIZE):
					for x in range(INPUT_GRID_SIZE-2, -1, -1):
						self.input_tiles[y][x+1] = self.input_tiles[y][x]
				for y in range(INPUT_GRID_SIZE):
					point  = (player_x-(self.tile_step)*64, player_y-(y-self.tile_step)*64)
					self.input_tiles[y][0] = self.get_tile_sort(point)
			
			#IF the player has gone down
			elif (self.last_position_y < player_y):				
				for x in range(INPUT_GRID_SIZE):
					for y in range(INPUT_GRID_SIZE-2, -1, -1):
						self.input_tiles[y+1][x] = self.input_tiles[y][x]
				for x in range(INPUT_GRID_SIZE):
					point  = (player_x-(x-self.tile_step)*64, player_y+(self.tile_step)*64)
					self.input_tiles[0][x] = self.get_tile_sort(point)
			#If the player has gone up
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

