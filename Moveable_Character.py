import arcade
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1
PLAYER_JUMP_SPEED = 18
ACCELERATION = 40
class Moveable_Character():

	def __init__(self, path_sprite,character_scaling, start_pos_x, start_pos_y):
		self.object_list = None
		self.path_sprite = path_sprite
		self.character_scaling = character_scaling
		self.object = None
		self.start_pos_y = start_pos_y
		self.start_pos_x = start_pos_x
		self.speed_x = 0
		self.physics = None
		self.jump_button_pressed = None
		self.left_button_pressed = None
		self.right_button_pressed =None

	def setup():
		self.object_list = arcade.SpriteList()
		self.object = arcade.Sprite(path_sprite, self.character_scaling)
		self.object.center_y = self.start_pos_y
		self.object.center_x = self.start_pos_x
		self.object_list.append(self.object)
		self.speed_x = 0
		self.jump_button_pressed = False
		self.left_button_pressed = False
		self.right_button_pressed = False



	def set_physics_engine(self, plattform_list):
		self.physics =  arcade.PhysicsEnginePlatformer(self.object, plattform_list, GRAVITY)


	#Function to update movement speed to include accerelation and deaccerelation
	def update_movement(self, delta_time):
		#Jump
		if self.jump_button_pressed:
			if self.physics.can_jump():
				self.player.change_y = PLAYER_JUMP_SPEED
				#self.score_minus += 1

		#Left button pressed accerelation
		if self.left_button_pressed and not self.right_button_pressed:
			self.speed_x -= ACCELERATION * delta_time

			#Check if speed is larger than max speed
			if(self.speed_x < -PLAYER_MOVEMENT_SPEED):
				self.speed_x = -PLAYER_MOVEMENT_SPEED
		
		#Left button released deaccerelation
		elif self.speed_x < 0:
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
		elif self.speed_x > 0:
			self.speed_x -= ACCELERATION * delta_time
			
			#Check for min speed
			if(self.speed_x < 0):
				self.speed_x = 0
		
		#Add the change to the sprite
		self.player.change_x = self.speed_x 