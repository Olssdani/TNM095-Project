'''
Game class
This class controlls everthing that has with the game to do.
The Neat algorithm is also contain inside this class
'''

#Imports
import arcade
import gc
import pickle
import neat
import Constant

from datetime import time
from neat.reporting import ReporterSet
from neat.math_util import mean
from neat.six_util import iteritems, itervalues
from arcade.arcade_types import Point
from Input import Input
from Score import Score
from Moveable_Character import Moveable_Character



#Scaling of sprites
TILE_SCALING = 0.5
CHARACTER_SCALING = 0.4
ENEMY_SCALING = 0.5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100
START_POSITION_X = 200

#NEAT constants
INPUT_GRID_SIZE = 9 #Keep uneven!!!
NO_IMPROVMENT_KILL = 150
MAX_GENERATIONS = 300

#Game Class
class Game(arcade.Window):
	#Constructor 
	def __init__(self, width, height, title):
		
		#Initalize parent object
		super().__init__(width, height, title, resizable=True)

		'''
		Initlization of member variables
		'''
		#Sprite lists
		self.plattform_list = None
		self.death_list = None
		self.end_list = None
		self.enemy_list = None
		self.background_list = None

		#Screen variables
		self.screen_width = width
		self.screen_height = height
		
		#Game specific variables
		self.game_over = False
		self.input = None

		#Moveable player
		self.ai =None
		self.player = None

		#Neat
		self.config_neat = None
		self.population = None
		self.gnomes = None
		self.current_genome_index = 0
		self.current_genome = None
		self.input_tiles = None
		self.network = None
		self.generation_counter = 1
		self.genome_id = 0
		self.type_of_run = None


	#Load population from file
	def start_from_file(self, filename):
		self.population = neat.Checkpointer.restore_checkpoint(filename)
		

	def setup_neat(self, config_file, run_setup): 
		self.config_neat = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
		self.type_of_run = run_setup
		
		#New Run
		if(run_setup == "n"):
			self.population = neat.Population(self.config_neat)	

		#Load generation from file
		elif (run_setup == "c"):
			print("Type generation number that should be load")
			input_generation_number = input()
			file_path ='neat-checkpoint-'+str(input_generation_number)
			self.start_from_file(file_path) 

		#Initalize population
		if(run_setup == "n" or run_setup =="c" ):
			self.genomes = list(iteritems(self.population.population))		
			
			# Add a stdout reporter to show progress in the terminal.
			self.population.add_reporter(neat.StdOutReporter(True))
			stats = neat.StatisticsReporter()
			self.population.add_reporter(stats)
			self.population.add_reporter(neat.Checkpointer(2))
			if self.population.config.no_fitness_termination and (MAX_GENERATIONS is None):
				raise RuntimeError("Cannot have no generational limit with no fitness termination")
		
		#Load in genome from file
		elif (self.type_of_run == "b"):
			self.current_genome = pickle.load(open( "winner.population", "rb" ))

		self.input_tiles = [[0 for x in range(INPUT_GRID_SIZE)] for y in range(INPUT_GRID_SIZE)]


	#Evolve gnomes
	def evolve_genomes(self):
		# Gather and report statistics.
		best = None
		for g in itervalues(self.population.population):
			if best is None or g.fitness > best.fitness:
				best = g	
		self.population.reporters.post_evaluate(self.population.config, self.population.population, self.population.species, best)

		# Keep track of the best genome.
		if self.population.best_genome is None or best.fitness > self.population.best_genome.fitness:
			self.population.best_genome = best

		if not self.population.config.no_fitness_termination:
			# End if the fitness threshold is reached.
			fv = self.population.fitness_criterion(g.fitness for g in itervalues(self.population.population))
			if fv >= self.population.config.fitness_threshold:
				self.population.reporters.found_solution(self.population.config, self.population.generation, best)
				pickle.dump(self.population.best_genome, open( "winner.population", "wb" ) )
				arcade.close_window()

		# Create the next generation from the current generation.
		self.population.population = self.population.reproduction.reproduce(self.population.config, self.population.species, self.population.config.pop_size, self.population.generation)

		# Check for complete extinction.
		if not self.population.species.species:
			self.population.reporters.complete_extinction()
			# If requested by the user, create a completely new population,
			# otherwise raise an exception.
			if self.population.config.reset_on_extinction:
				self.population.population = self.population.reproduction.create_new(self.population.config.genome_type, self.population.config.genome_config, self.population.config.pop_size)
			else:
				raise CompleteExtinctionException()

		# Divide the new population into species.
		self.population.species.speciate(self.population.config, self.population.population, self.population.generation)
		self.population.reporters.end_generation(self.population.config, self.population.population, self.population.species)
		self.population.generation += 1
		

	def setup(self):
		#Initialize the sprite lists
		self.plattform_list = arcade.SpriteList()
		self.death_list = arcade.SpriteList()
		self.end_list = arcade.SpriteList()
		self.enemy_list = arcade.SpriteList()
		self.background_list = arcade.SpriteList()

		#Initalize the player sprite and vairables
		self.ai = Moveable_Character("Ai.png", CHARACTER_SCALING, START_POSITION_X, 200)
		self.player = Moveable_Character("Player.png", CHARACTER_SCALING, START_POSITION_X, 200)

		#Name of level file
		map_name = "Level1.tmx"
		
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
		
		#Initialize the input class with the right sprite list
		self.input = Input(INPUT_GRID_SIZE, self.plattform_list, self.enemy_list, Constant.TILE_SIZE)

		#Set the movement for the enemies
		for enemy in self.enemy_list:
			enemy.change_x = 2

		# Set the background color
		if my_map.background_color:	
			arcade.set_background_color(my_map.background_color)

		# Create the 'physics engine'
		self.ai.set_physics_engine(self.plattform_list)
		self.player.set_physics_engine(self.plattform_list)

		#Used to keep track of our scrolling
		self.view_bottom = 0
		self.view_left = 0

		#If not running a best genome run evolve the population
		if(self.type_of_run != "b" and self.current_genome_index > len(self.genomes) - 1):
			self.evolve_genomes()

			self.genomes = list(iteritems(self.population.population))

			self.current_genome_index = 0
		#If first genome in generation start reporters
		if(self.current_genome_index == 0 and self.type_of_run != "b"):
			self.population.reporters.start_generation(self.population.generation)
		#Update genome
		if(self.type_of_run != "b"):
			self.current_genome = self.genomes[self.current_genome_index][1]
			self.genome_id = self.genomes[self.current_genome_index][0]

		#get network
		self.network = neat.nn.recurrent.RecurrentNetwork.create(self.current_genome, self.config_neat)
		

	#Draw call
	def on_draw(self):

		arcade.start_render()
		
		self.plattform_list.draw()
		self.ai.draw()
		if(self.type_of_run == "b"):
			self.player.draw()
		self.death_list.draw()
		self.end_list.draw()
		self.enemy_list.draw()
		self.background_list.draw()
		

		# Draw our score on the screen, scrolling it with the viewport
		if(self.type_of_run != "b"):
			score_text = f"Score: {self.ai.get_score_object().get_score()}"
		else:
			score_text = f"Score: {self.player.get_score_object().get_score()}"

		arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.WHITE, 18)


	#Resize window
	def on_resize(self, width, height):
		super().on_resize(width, height)
		self.screen_width = width
		self.screen_height = height


	def on_key_press(self, key, modifiers):
		if key == arcade.key.UP or key == arcade.key.W:
			self.player.jump_button_pressed = True
		if key == arcade.key.LEFT or key == arcade.key.A:
			self.player.left_button_pressed = True
		if key == arcade.key.RIGHT or key == arcade.key.D:
			self.player.right_button_pressed = True


	def on_key_release(self, key, modifiers):
		if key == arcade.key.UP or key == arcade.key.W:
			self.player.jump_button_pressed = False
		if key == arcade.key.LEFT or key == arcade.key.A:
			self.player.left_button_pressed = False
		elif key == arcade.key.RIGHT or key == arcade.key.D:
			self.player.right_button_pressed = False


	#Scroll viewport
	def scrolling(self, object):	
		# Track if we need to change the viewport
		changed = False

		# Scroll left
		left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN	
		if object.left < left_boundary:
			self.view_left -= left_boundary - object.left
			changed = True

		# Scroll right
		right_boundary = self.view_left + self.screen_width - RIGHT_VIEWPORT_MARGIN
		if object.right > right_boundary:
			self.view_left += object.right - right_boundary
			changed = True

		# Scroll up
		top_boundary = self.view_bottom + self.screen_height - TOP_VIEWPORT_MARGIN
		if object.top > top_boundary:
			self.view_bottom += object.top - top_boundary
			changed = True

		# Scroll down
		bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
		if object.bottom < bottom_boundary and object.bottom>BOTTOM_VIEWPORT_MARGIN:
			self.view_bottom -= bottom_boundary - object.bottom
			changed = True

		if changed:
			# Only scroll to integers. Otherwise we end up with pixels that
			# don't line up on the screen
			self.view_bottom = int(self.view_bottom)
			self.view_left = int(self.view_left)

			# Do the Scrolling
			arcade.set_viewport(self.view_left, self.screen_width + self.view_left, self.view_bottom, self.screen_height + self.view_bottom)


	#Update all sprites		
	def update(self, delta_time):
		should_end = False

		#Create a list of the input matrix
		inputs = list(())
		self.input_tiles = self.input.get_input_tiles(self.ai.object.center_x, self.ai.object.center_y)
		for y in range(INPUT_GRID_SIZE):
			for x in range(INPUT_GRID_SIZE):
				inputs.append(self.input_tiles[y][x])
	
		#Calculate the outputs.
		nnOutput = self.network.activate(inputs)
		self.ai.left_button_pressed = round(nnOutput[0])
		self.ai.jump_button_pressed = round(nnOutput[1])
		self.ai.right_button_pressed = round(nnOutput[2])

		#Update the movement on the player
		self.ai.update_movement(delta_time)
		self.player.update_movement(delta_time)
			
		# Move the enemies
		self.enemy_list.update()

		for enemy in self.enemy_list:
			# If the enemy hit a wall, reverse
			if len(arcade.check_for_collision_with_list(enemy, self.plattform_list)) > 0:
				enemy.change_x *= -1
			
		# Update the player using the physics engine
		self.ai.physics.update()
		self.player.physics.update()

		#If training network
		if(self.type_of_run != "b"):
			
			# See if the player hit a enemy, just restart 
			if len(arcade.check_for_collision_with_list(self.ai.object, self.enemy_list)) > 0:
				should_end = True
			if arcade.check_for_collision_with_list(self.ai.object, self.death_list):
				should_end = True
			if arcade.check_for_collision_with_list(self.ai.object, self.end_list):
				self.ai.get_score_object.add_to_score(1000)
				should_end = True
			
			self.scrolling(self.ai.object)
			
			self.ai.get_score_object().update_score(self.ai.object.center_x)

			if self.ai.get_score_object().get_highscore_still() > NO_IMPROVMENT_KILL:
				should_end = True
			if should_end:
				
				self.genomes[self.current_genome_index][1].fitness = self.ai.get_score_object().get_score()
				print("On genome id: " + str(self.genome_id) + " with fitness: " + str(self.genomes[self.current_genome_index][1].fitness))
				self.current_genome_index +=1
				self.setup()
		#If playing best network
		else:
			# See if the player hit a enemy, just restart 
			if len(arcade.check_for_collision_with_list(self.ai.object, self.enemy_list)) > 0:
				self.ai.show = False
			if arcade.check_for_collision_with_list(self.ai.object, self.death_list):
				self.ai.show = False
			if arcade.check_for_collision_with_list(self.ai.object, self.end_list):
				self.ai.show = False

			if len(arcade.check_for_collision_with_list(self.player.object, self.enemy_list)) > 0:
				should_end = True
			if arcade.check_for_collision_with_list(self.player.object, self.death_list):
				should_end = True
			if arcade.check_for_collision_with_list(self.player.object, self.end_list):
				should_end = True

			self.scrolling(self.player.object)
			self.player.get_score_object().update_score(self.player.object.center_x)
			
			if should_end:
				self.setup()
		

	def run(self):
		arcade.run()
		
