#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

import NPNG
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
STATE_PAUSE = 1
STATE_READY = 2

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

	
def main_game_update(arena,line, player):

	# increase the angle of the rotating line
	line.angle = (line.angle + 1)

	# the rotating line angle ranges between 90 and 180 degrees
	if line.angle > 179:

		# when it reaches an angle of 180 degrees, reposition the circular hitbox
		
		##player.location = (random.randint(arena.area[0][0],arena.area[0][1]),random.randint(arena.area[1][0],arena.area[1][1]))
		
		line.angle = 0
	

	# the points associated with each line segment must be recalculated as the angle changes
	line.segments = []
	
	# consider every line segment length
	line.compute_line(arena)
	
	# start by assuming that no collisions have occurred
	player.collision = False
	
	# consider possible collisions between the circle hitbox and each line segment
	line.check_collision(player)

	# return the new state of the rotating line and the circle hitbox
	return line, player
	
#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####


	
#### ====================================================================================================================== ####
#############                                            RENDER                                                    #############
#### ====================================================================================================================== ####
	
def main_menu_render(window_sfc, start_button):

	# clear the window surface (by filling it with black)
	window_sfc.fill( (255,0,0) )
	
	myfont = pygame.font.SysFont('Impact', 60)
	textsurface = myfont.render('No Pain No Gain', False, (0, 0, 0))
	window_sfc.blit(textsurface,(250, 100))
	
	start_button.render(window_sfc)
	
def main_game_render(arena,line, player, window_sfc):

	# clear the window surface (by filling it with black)
	window_sfc.fill( (0,0,0) )
	
	arena.render(window_sfc)
	
	line.render(window_sfc)
	
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
	start_button = NPNG.Button([(window_sfc.get_width()/2-50,window_sfc.get_height()/2-50),(100,100)])
	arena = NPNG.Arena([(250),((window_wid // 2), (window_hgt // 2)-50)])
	

	# this game object is a line segment, with a single gap, rotating around a point
	# the "origin" around which the line rotates,the current "angle" of the line the "length" intervals that specify the gap(s),
	# the individual "segments" (i.e., non-gaps)
	line = NPNG.Line([(arena.location),0,[(-1.00, -0.50),(-0.25, 0.25),(0.50, 1.00)],[],1])
	
	# this game object is a circular
	player = NPNG.Player([((window_wid // 2)-100, (window_hgt // 2)+100),15,False])
	
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
				next_state = STATE_READY
			
		if (game_state == STATE_READY):
		
			player.check_moving(arena)
			closed_flag = quit()
		
		#####################################################################################################
		# this is the "update" phase of the game loop, where the changes to the game world are handled
		#####################################################################################################
		if (game_state == STATE_READY):
		
			line, player = main_game_update(arena,line, player) 
			player.move(arena)
		
		#####################################################################################################
		# this is the "render" phase of the game loop, where a representation of the game world is displayed
		#####################################################################################################
		if (game_state == STATE_TITLE):
		
			main_menu_render(window_sfc,start_button)
			
			
		if (game_state == STATE_READY):
		
			main_game_render(arena,line, player, window_sfc)
			
		# update the display
		pygame.display.update()
		
		#set the game to the next state
		game_state = next_state
		
		# enforce the minimum frame rate
		clock.tick(frame_rate)
		
		
if __name__ == "__main__":
	main()
