'''
Moveable Character class
This class handles all functionality of a sprite that can be moved
either by player or AI
'''

import arcade
import Constant

#Class specific constants
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1
PLAYER_JUMP_SPEED = 18
ACCELERATION = 40

from Score import Score 
class Moveable_Character():

	def __init__(self, path_sprite,character_scaling, start_pos_x, start_pos_y):
		self.object_list = arcade.SpriteList()
		self.object = arcade.Sprite(path_sprite, character_scaling)
		self.object.center_y = start_pos_y
		self.object.center_x = start_pos_x
		self.object_list.append(self.object)
		self.speed_x = 0
		self.physics = None
		self.jump_button_pressed = False
		self.left_button_pressed = False
		self.right_button_pressed = False
		self.score = Score(start_pos_x, Constant.TILE_SIZE)
		self.show = True


	def set_physics_engine(self, plattform_list):
		self.physics =  arcade.PhysicsEnginePlatformer(self.object, plattform_list, GRAVITY)


	#Function to update movement speed to include accerelation and deaccerelation
	def update_movement(self, delta_time):
		
		#If object should be rendered
		if self.show:
			#Jump
			if self.jump_button_pressed:
				if self.physics.can_jump():
					self.object.change_y = PLAYER_JUMP_SPEED

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
			self.object.change_x = self.speed_x


	def draw(self):
		if(self.show):
			self.object_list.draw()


	def get_score_object(self):
		return self.score