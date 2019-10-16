class Score():
	
	def __init__(self, start_position_x, tile_size):
		self.distance_score = 0
		self.plus_score = 0
		self.minus_score = 0
		self.final_score = 0
		self.start_position_x = start_position_x
		self.tile_size = tile_size
		self.counter = 0


	#Update the score depending on the distance
	def update_score(self, player_postion_x):
	 	new_score =int((player_postion_x-self.start_position_x) / self.tile_size)
	 	
	 	#Make sure that the score does not decrease if going backwards and count the 
	 	#frames that the AI does not move
	 	if new_score>self.distance_score:
	 		self.distance_score = new_score
	 		self.counter = 0
	 	else:
	 		self.counter +=1 
		
	def add_to_score(self, points):
		self.plus_score += points


	def minus_to_score(self, points):
		self.minus_score += points


	def get_highscore_still(self):
		return self.counter


	def get_score(self):
		return self.distance_score + self.plus_score - self.minus_score
