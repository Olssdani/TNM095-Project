import arcade


TILESCALING = 0.5
CHARACTERSCALING = 1.0


class Game(arcade.Window):
	def __init__(self, width, height, title):
		super().__init__(width, height, title, resizable=True)
		arcade.set_background_color(arcade.color.AMAZON)
		self.groundList = None


	def setup(self):
		#Setup the list
		self.groundList = arcade.SpriteList()

		# Create the ground
		for x in range(0, 1250, 64):
			ground = arcade.Sprite("Sprites/Used/ground05.png", TILESCALING)
			ground.center_x = x
			ground.center_y = 32
			self.groundList.append(ground)

		# Create the ground
		for x in range(0, 1250, 64):
			ground = arcade.Sprite("Sprites/Used/leafy_ground01.png", TILESCALING)
			ground.center_x = x
			ground.center_y = 96
			self.groundList.append(ground)



	def on_draw(self):

		arcade.start_render()
		arcade.draw_circle_filled(420, 285, 18, arcade.color.GREEN)
		self.groundList.draw()


	#Resize the window if user wants
	def on_resize(self, width, height):
		super().on_resize(width, height)


	def update(self, delta_time):
		pass
