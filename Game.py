import arcade
from datetime import time

#Scaling of sprites
TILE_SCALING = 0.5
CHARACTERSCALING = 0.4
ENEMYSCALING = 0.5

#Player Constants!
PLAYERMOVEMENTSPEED = 7
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

class Game(arcade.Window):
	def __init__(self, width, height, title):
		super().__init__(width, height, title, resizable=True)
		arcade.set_background_color(arcade.color.AMAZON)
		self.groundList = None
		self.playerList = None
		self.deathList = None
		self.end_list = None
		self.enemy_list = None
		self.Screen_Width = width
		self.Screen_Height = height
		self.right_button_pressed = False
		self.left_button_pressed = False
		self.jump_button_pressed = False
		self.speed_x = 0
		self.game_over = False
		self.score_distance = 0

	def setup(self):
		#Setup the list
		self.groundList = arcade.SpriteList()
		self.playerList = arcade.SpriteList()
		self.deathList = arcade.SpriteList()
		self.end_list = arcade.SpriteList()
		self.enemy_list = arcade.SpriteList()

		self.player = arcade.Sprite("Sprites/Used/Player.png", CHARACTERSCALING)
		self.player.center_y = 200
		self.player.center_x = START_POSITION_X
		self.playerList.append(self.player)
		self.score_distance = 0
		self.speed_x = 0


		# --- Load in a map from the tiled editor ---
		# Name of map file to load
		map_name = "Level1.tmx"
		# Names of the layers
		platforms_layer_name = 'Plattform'
		death_layer_name = 'Death'
		end_layer_name = 'End'
		enemy_layer_name = 'Enemy'

		# Read in the tiled map
		my_map = arcade.tilemap.read_tmx(map_name)

		# Read the tilemaps
		self.groundList = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
		self.deathList = arcade.tilemap.process_layer(my_map, death_layer_name, TILE_SCALING)
		self.end_list = arcade.tilemap.process_layer(my_map, end_layer_name, TILE_SCALING)
		self.enemy_list = arcade.tilemap.process_layer(my_map, enemy_layer_name, ENEMYSCALING)

		for enemy in self.enemy_list:
			enemy.change_x = 2

		# Set the background color
		if my_map.background_color:	
			arcade.set_background_color(my_map.background_color)

		# Create the 'physics engine'
		self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.groundList, GRAVITY)
		#Used to keep track of our scrolling
		self.view_bottom = 0
		self.view_left = 0


	def on_draw(self):
		#Start the rendering
		arcade.start_render()
		#Draw the objects
		self.groundList.draw()
		self.playerList.draw()
		self.deathList.draw()
		self.end_list.draw()
		self.enemy_list.draw()
		 # Draw our score on the screen, scrolling it with the viewport
		score_text = f"Score: {self.score_distance}"
		arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)



	#Resize the window if user wants
	def on_resize(self, width, height):
		super().on_resize(width, height)
		self.Screen_Width = width
		self.Screen_Height = height


	def on_key_press(self, key, modifiers):
		"""Called whenever a key is pressed. """
		if key == arcade.key.UP or key == arcade.key.W:
			self.jump_button_pressed = True
		if key == arcade.key.LEFT or key == arcade.key.A:
			self.left_button_pressed = True
			self.player.change_x = -PLAYERMOVEMENTSPEED
		if key == arcade.key.RIGHT or key == arcade.key.D:
			self.right_button_pressed = True
			self.player.change_x = PLAYERMOVEMENTSPEED


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

			#Add movement to sprite and check if movementspeed is outside limits
			if(self.speed_x < -PLAYERMOVEMENTSPEED):
				self.speed_x = -PLAYERMOVEMENTSPEED
		#Left button released deaccerelation
		elif self.speed_x <0 and not self.right_button_pressed:
			self.speed_x += ACCELERATION * delta_time
			if(self.speed_x > 0):
				self.speed_x = 0
		

		#Right button pressed accerelation
		if self.right_button_pressed and not self.left_button_pressed:
			self.speed_x += ACCELERATION * delta_time

			#Add movement to sprite
			if(self.speed_x > PLAYERMOVEMENTSPEED):
				self.speed_x = PLAYERMOVEMENTSPEED
		#Right button released and deaccerelation
		elif self.speed_x> 0 and not self.left_button_pressed:
			self.speed_x -= ACCELERATION * delta_time
			if(self.speed_x < 0):
				self.speed_x = 0
		#Add the speed to the sprite
		self.player.change_x = self.speed_x 
		print(self.speed_x)


	def update_score(self):
	 	new_score =int((self.player.center_x-START_POSITION_X) / 64)
	 	if new_score>self.score_distance:
	 		self.score_distance = new_score
		


	def scrolling(self):
		# --- Manage Scrolling ---

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

	def update(self, delta_time):
		""" Movement and game logic """

		# Call update on all sprites (The sprites don't do much in this
		# example though.)
		self.update_movement(delta_time)
		#self.physics_engine.update()
		#self.enemy_list.update()

		 # Update the player based on the physics engine
		if not self.game_over:
			# Move the enemies
			self.enemy_list.update()

			# Check each enemy
			for enemy in self.enemy_list:
				# If the enemy hit a wall, reverse
				if len(arcade.check_for_collision_with_list(enemy, self.groundList)) > 0:
					enemy.change_x *= -1
			# Update the player using the physics engine
			self.physics_engine.update()

			# See if the player hit a worm. If so, game over.
			if len(arcade.check_for_collision_with_list(self.player, self.enemy_list)) > 0:
				self.setup()
			if arcade.check_for_collision_with_list(self.player, self.deathList):
				self.setup()
			if arcade.check_for_collision_with_list(self.player, self.end_list):
				self.setup()

		self.scrolling()
		self.update_score()

		