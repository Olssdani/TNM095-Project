import arcade


TILESCALING = 0.5
CHARACTERSCALING = 0.5
PLAYERMOVEMENTSPEED = 5

class Game(arcade.Window):
	def __init__(self, width, height, title):
		super().__init__(width, height, title, resizable=True)
		arcade.set_background_color(arcade.color.AMAZON)
		self.groundList = None
		self.playerList = None


	def setup(self):
		#Setup the list
		self.groundList = arcade.SpriteList()
		self.playerList = arcade.SpriteList()


		#Variable for the player sprite
		# Separate variable that holds the player sprite
		self.player = None
		
		# Create the ground
		for x in range(0, 1250, 64):
			ground = arcade.Sprite("Sprites/Used/ground05.png", TILESCALING)
			ground.center_x = x
			ground.center_y = 32
			self.groundList.append(ground)

		for x in range(0, 1250, 64):
			ground = arcade.Sprite("Sprites/Used/leafy_ground01.png", TILESCALING)
			ground.center_x = x
			ground.center_y = 96
			self.groundList.append(ground)

		self.player = arcade.Sprite("Sprites/Used/Player.png", CHARACTERSCALING)
		self.player.center_y = 420
		self.player.center_x = 285
		self.playerList.append(self.player)

		# Create the 'physics engine'
		self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.groundList)

	def on_draw(self):

		arcade.start_render()
		self.groundList.draw()
		self.playerList.draw()




	#Resize the window if user wants
	def on_resize(self, width, height):
		super().on_resize(width, height)

	def on_key_press(self, key, modifiers):
		"""Called whenever a key is pressed. """

		if key == arcade.key.UP or key == arcade.key.W:
			self.player.change_y = PLAYERMOVEMENTSPEED
		elif key == arcade.key.DOWN or key == arcade.key.S:
			self.player.change_y = -PLAYERMOVEMENTSPEED
		elif key == arcade.key.LEFT or key == arcade.key.A:
			self.player.change_x = -PLAYERMOVEMENTSPEED
		elif key == arcade.key.RIGHT or key == arcade.key.D:
			self.player.change_x = PLAYERMOVEMENTSPEED

	def on_key_release(self, key, modifiers):
		"""Called when the user releases a key. """

		if key == arcade.key.UP or key == arcade.key.W:
			self.player.change_y = 0
		elif key == arcade.key.DOWN or key == arcade.key.S:
			self.player.change_y = 0
		elif key == arcade.key.LEFT or key == arcade.key.A:
			self.player.change_x = 0
		elif key == arcade.key.RIGHT or key == arcade.key.D:
			self.player.change_x = 0

	def update(self, delta_time):
		""" Movement and game logic """

		# Call update on all sprites (The sprites don't do much in this
		# example though.)
		self.physics_engine.update()
