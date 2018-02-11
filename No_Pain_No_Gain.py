#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

import screens
import entitys
import pygame
import random
import math

from pygame.locals import *
pygame.font.init()	# you have to call this at the start, 
					# if you want to use this module.

# the window is the actual window onto which the camera view is resized and blitted
window_wid = 1200
window_hgt = 600

# the frame rate is the number of frames per second that will be displayed and although
# we could (and should) measure the amount of time elapsed, for the sake of simplicity
# we will make the (not unreasonable) assumption that this "delta time" is always 1/fps
frame_rate = 40
delta_time = 1 / frame_rate


# constants for designating the different games states
STATE_TITLE = 0
STATE_CUTSCENE = 1
STATE_ROOM = 2
STATE_GAME = 3
STATE_WIN = 4
STATE_REST = 5
STATE_END = 9

#### ====================================================================================================================== ####
#############                                           PROCESS                                                    #############
#### ====================================================================================================================== ####

	
def quit():

	# look in the event queue for the quit event
	quit_ocrd = False
	for event in pygame.event.get():
		if event.type == QUIT:
			quit_ocrd = True
		
		if event.type == pygame.KEYDOWN:
			if(pygame.K_ESCAPE == event.key):
				quit_ocrd = True
		
	return quit_ocrd

#### ====================================================================================================================== ####
#############                                            UPDATE                                                    #############
#### ====================================================================================================================== ####

	
def main_game_update(arena,line, player,goal):

	# increase the angle of the rotating line
	line.move_line()

	# the rotating line angle ranges between 90 and 180 degrees
	if line.angle > 179:

		# when it reaches an angle of 180 degrees, reposition the circular hitbox
		
		##player.location = (random.randint(arena.area[0][0],arena.area[0][1]),random.randint(arena.area[1][0],arena.area[1][1]))
		goal.new(arena)
		line.angle = 0
	
	# consider every line segment length
	line.compute(arena)
	
	# consider possible collisions between the circle hitbox and each line segment
	line.check_collision(player)
	
	#check if player got a point
	player.check_goal(goal,arena)

	# return the new state of the rotating line and the circle hitbox
	return line, player, goal
	
#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####


	
#### ====================================================================================================================== ####
#############                                            RENDER                                                    #############
#### ====================================================================================================================== ####
	
def tittle_screen_render(window_sfc, start_button):

	# clear the window surface (by filling it with black)
	window_sfc.fill( (255,0,0) )
	
	myfont = pygame.font.SysFont('Impact', 60)
	textsurface = myfont.render('No Pain No Gain', False, (0, 0, 0))
	window_sfc.blit(textsurface,(250, 100))
	
	start_button.render(window_sfc)
	
def main_game_render(arena,line, player,goal, window_sfc):

	# clear the window surface (by filling it with black)
	window_sfc.fill( (0,0,0) )
	
	arena.render(window_sfc)
	
	line.render(window_sfc)
	
	goal.render(window_sfc)
	
	player.render(window_sfc)
	
#### ====================================================================================================================== ####
#############                                             MAIN                                                     #############
#### ====================================================================================================================== ####

def main():
	
	# initialize pygame
	pygame.init()
	
	# create the window and set the caption of the window
	window_sfc = pygame.display.set_mode( (window_wid, window_hgt) )
	pygame.display.set_caption('No Pain No Gain')
	
	# create a clock
	clock = pygame.time.Clock()
	
	# this is the initial game state
	next_state = STATE_TITLE

	#####################################################################################################
	# these are the initial game objects that are required (in some form) for the core mechanic provided
	#####################################################################################################
	start_button = entitys.Button([(window_sfc.get_width()/2-50,window_sfc.get_height()/2-50),(100,100)])
	arena = entitys.Arena([(250),((window_wid // 2), (window_hgt // 2)-50),10])
	
	continue_button = entitys.Button([(window_sfc.get_width()/2-50,window_sfc.get_height()/2-50),(100,100)])
	cutscene = screens.Screen(["cutscene",continue_button,"No Input",None,1])
	
	play_button = entitys.Button([(window_sfc.get_width()/2-50,window_sfc.get_height()/2-50),(100,100)])
	room = screens.Screen(["room",play_button,"No Input",None,3])
	
	

	# this game object is a line segment, with a single gap, rotating around a point
	# the "origin" around which the line rotates,the current "angle" of the line the "length" intervals that specify the gap(s),
	# the individual "segments" (i.e., non-gaps)
	line = entitys.Line([(arena.location),0,[(-1.00, -0.50),(-0.30, 0.30),(0.50, 1.00)],[],1,1])
	
	# this game object is a circular
	player = entitys.Player([((window_wid // 2)-100, (window_hgt // 2)+100)])
	
	#the is a goal for the player to touch to receive points
	goal = entitys.Goal([((window_wid // 2)-100, (window_hgt // 2)+100),10,False,2],arena)

	
	game_state = next_state
	
	# the game loop is a postcondition loop controlled using a Boolean flag
	closed_flag = False
	while not closed_flag:

			
		#####################################################################################################
		# this is the "inputs" phase of the game loop, where player input is retrieved and stored
		#####################################################################################################
		if (game_state == STATE_TITLE):
			
			closed_flag = quit()
			if (start_button.clicked()[0]):
				next_state = STATE_GAME
			
		elif (game_state == STATE_GAME):
		
			player.check_moving(arena)
			closed_flag = quit()
			
		elif (game_state == STATE_CUTSCENE):
		
			if(cutscene.check_button()):
				next_state = cutscene.next_screen
			closed_flag = quit()
			
		elif (game_state == STATE_ROOM):
		
			if(room.check_button()):
				next_state = room.next_screen
			closed_flag = quit()
		#####################################################################################################
		# this is the "update" phase of the game loop, where the changes to the game world are handled
		#####################################################################################################
		if (game_state == STATE_GAME):
		
			line, player, goal = main_game_update(arena,line, player,goal) 
			player.move(arena)
			#check if the player won
			if (arena.check(player,cutscene)):
				next_state = STATE_CUTSCENE
		
		#####################################################################################################
		# this is the "render" phase of the game loop, where a representation of the game world is displayed
		#####################################################################################################
		if (game_state == STATE_TITLE):
		
			tittle_screen_render(window_sfc,start_button)
		
		elif (game_state == STATE_ROOM):
		
			room.render(window_sfc)
			
		elif (game_state == STATE_GAME):
		
			main_game_render(arena,line, player,goal, window_sfc)
			
		elif (game_state == STATE_CUTSCENE):
		
			cutscene.render(window_sfc)
			
		# update the display
		pygame.display.update()
		
		#set the game to the next state
		game_state = next_state
		
		# enforce the minimum frame rate
		clock.tick(frame_rate)
		
		
if __name__ == "__main__":
	main()
