'''
This file has the functionality to get the inputs around 
'''
import arcade
import Constant



class Input():
	#Constructor 
	def __init__(self, grid_size, plattform_list, enemy_list, tile_size):
		self.grid_size = grid_size
		self.plattform_list = plattform_list
		self.enemy_list = enemy_list
		self.tile_size = tile_size
		self.tile_step = self.grid_size//2
		self.last_position_x = 0
		self.last_position_y = 0
		self.input_tiles = [[0 for x in range(self.grid_size)] for y in range(self.grid_size)]

	#Return value for the tile depending on whats on that tile
	def get_tile_sort(self, point):
		#Value for the tiles is hostile =-1, nothing = 0 and plattform =1
		if len(arcade.get_sprites_at_point(point, self.plattform_list)) > 0:
			return Constant.PLATTFORM
		else:
			return Constant.NOTHING

	#Get tiles in a surrounding area around the player as input. Each tile corresponds to
	#a number where platfrom = 1, nothing = 0 and enemy = -1. Number of tiles is controlled
	#by the constant variable self.grid_size
	def get_input_tiles(self, position_x, position_y):
		#Get the tile position that the player is on. The player position is clamp to an int and
		#is offset to half a tile size to get it to the center position
		player_x = (position_x // self.tile_size ) * self.tile_size + self.tile_size/2
		player_y = (position_y // self.tile_size ) * self.tile_size + self.tile_size/2
		
		for y in range(self.grid_size):
			for x in range(self.grid_size):
				point  = (player_x+(x-self.tile_step)*self.tile_size, player_y-(y-self.tile_step)*self.tile_size)
				if(len(arcade.get_sprites_at_point(point, self.enemy_list)) > 0):
					self.input_tiles[y][x] = -1
				elif(self.input_tiles[y][x] < 0):
					self.input_tiles[y][x] = 0
		#Check if player have moved into another tile otherwise do not update the input tiles
		if(self.last_position_y !=player_y or self.last_position_x != player_x):
			
			#If player has moved into another square in both directions, update the whole tile set
			#TODO optimize this by push the current tiles and just update the outer tiles	
			if(self.last_position_y !=player_y and self.last_position_x != player_x):
				for y in range(self.grid_size):
					for x in range(self.grid_size):
						point  = (player_x+(x-self.tile_step)*self.tile_size, player_y-(y-self.tile_step)*self.tile_size)
						self.input_tiles[y][x] = self.get_tile_sort(point)			
			
			#If the player has moved to the right
			elif (self.last_position_x < player_x):
				#Push the input tiles so only the outer tiles need to update
				for y in range(self.grid_size):
					for x in range(1,self.grid_size):
						self.input_tiles[y][x-1] = self.input_tiles[y][x]
				#Update the outer tiles
				for y in range(self.grid_size):
					point  = (player_x+(self.tile_step)*self.tile_size, player_y-(y-self.tile_step)*self.tile_size)
					self.input_tiles[y][self.grid_size-1] = self.get_tile_sort(point)
			
			#If the player has moved to the left
			elif (self.last_position_x > player_x):
				for y in range(self.grid_size):
					for x in range(self.grid_size-2, -1, -1):
						self.input_tiles[y][x+1] = self.input_tiles[y][x]
				for y in range(self.grid_size):
					point  = (player_x-(self.tile_step)*self.tile_size, player_y-(y-self.tile_step)*self.tile_size)
					self.input_tiles[y][0] = self.get_tile_sort(point)
			
			#IF the player has gone down
			elif (self.last_position_y < player_y):				
				for x in range(self.grid_size):
					for y in range(self.grid_size-2, -1, -1):
						self.input_tiles[y+1][x] = self.input_tiles[y][x]
				for x in range(self.grid_size):
					point  = (player_x-(x-self.tile_step)*self.tile_size, player_y+(self.tile_step)*self.tile_size)
					self.input_tiles[0][x] = self.get_tile_sort(point)
			#If the player has gone up
			elif (self.last_position_y > player_y):		
				for x in range(self.grid_size):
					for y in range(self.grid_size-1):
						self.input_tiles[y][x] = self.input_tiles[y + 1][x]
				for x in range(self.grid_size):
					point  = (player_x + (x - self.tile_step) * self.tile_size, player_y - self.tile_step * self.tile_size)
					self.input_tiles[self.grid_size-1][x] = self.get_tile_sort(point)
		
		#Update last postion
		self.last_position_x = player_x
		self.last_position_y = player_y
	
		return self.input_tiles


	#Print the input tiles in the console, used for debug
	def print_input_tile(self):
		#Print tile, for debug use only
		for y in range(self.grid_size):
			for x in range(self.grid_size):
				if(x == self.grid_size-1):
					print(self.input_tiles[y][x])
				else:
					print(self.input_tiles[y][x], end=' ')


		print(" ")

