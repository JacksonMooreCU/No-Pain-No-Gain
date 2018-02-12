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
STATE_END = 99
	
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
	title = screens.Screen(["tittle",start_button,"No Pain No Gain",None,3])
	
	arena0 = entitys.Arena([(250),((window_wid // 2), (window_hgt // 2)-50),10])
	
	continue_button = entitys.Button([(window_sfc.get_width()/2-50,window_sfc.get_height()/2-50),(100,100)])
	cutscene = screens.Screen(["cutscene",continue_button,"No Input",None,1])
	
	battle_button = entitys.Button([(window_sfc.get_width()/2-200,window_sfc.get_height()/2-100),(100,100)])
	train_button = entitys.Button([(window_sfc.get_width()/2,window_sfc.get_height()/2-100),(100,100)])
	sleep_button = entitys.Button([(window_sfc.get_width()/2+200,window_sfc.get_height()/2-100),(100,100)])
	room = screens.Menu(["room",[battle_button,train_button,sleep_button],"Battle, Train, or Rest?",[3,3,2]])

	# this game object is a line segment, with a single gap, rotating around a point
	# the "origin" around which the line rotates,the current "angle" of the line the "length" intervals that specify the gap(s),
	# the individual "segments" (i.e., non-gaps)
	line0 = entitys.Line([(arena0.location),0,[(-1.00, -0.50),(-0.30, 0.30),(0.50, 1.00)],[],1,1])
	line1 = entitys.Line([(arena0.location),0,[(-1.00, -0.50),(-0.30, 0.30),(0.50, 1.00)],[],1,-1])
	
	# this game object is a circular
	player = entitys.Player([((window_wid // 2)-100, (window_hgt // 2)+100)])
	
	#the is a goal for the player to touch to receive points
	goal0 = entitys.Goal([((window_wid // 2)-100, (window_hgt // 2)+100),10,False,2],arena0)
	
	#battle 0 screen
	battle0 = screens.Battle(["battle",arena0,[line0,line1],goal0])

	
	game_state = next_state
	
	# the game loop is a postcondition loop controlled using a Boolean flag
	closed_flag = False
	while not closed_flag:

			
		#####################################################################################################
		# this is the "inputs" phase of the game loop, where player input is retrieved and stored
		#####################################################################################################
		if (game_state == STATE_TITLE):
			
			closed_flag = title.quit()
			if (title.check_button()):
				next_state = STATE_ROOM
			
		elif (game_state == STATE_GAME):
		
			player.check_moving(battle0.arena)
			closed_flag = battle0.quit()
		
			
		elif (game_state == STATE_CUTSCENE):
		
			if(cutscene.check_button()):
				next_state = cutscene.next_screen
				
			closed_flag = cutscene.quit()
			
		elif (game_state == STATE_ROOM):
		
			if(room.check_buttons(player)):
				next_state = room.next_screen
			closed_flag = room.quit()
			
		#####################################################################################################
		# this is the "update" phase of the game loop, where the changes to the game world are handled
		#####################################################################################################
		if (game_state == STATE_GAME):
	
			battle0.update(player)
			
			#check if the player won
			if (battle0.arena.check(player,cutscene)):
				next_state = STATE_CUTSCENE
				
		# if the player lost exit loop
		if (game_state == STATE_END): 
			closed_flag = True
		
		#####################################################################################################
		# this is the "render" phase of the game loop, where a representation of the game world is displayed
		#####################################################################################################
		if (game_state == STATE_TITLE):
		
			title.render(window_sfc)
		
		elif (game_state == STATE_ROOM):
		
			room.render(player,window_sfc)
			
		elif (game_state == STATE_GAME):
		
			battle0.render(player,window_sfc)
			
		elif (game_state == STATE_CUTSCENE):
		
			cutscene.render(window_sfc)
			
		# update the display
		pygame.display.update()
		
		#set the game to the next state
		game_state = next_state
		
		# enforce the minimum frame rate
		clock.tick(frame_rate)
		
	# if the player lost re run the game
	if (game_state == STATE_END): 
		main()
if __name__ == "__main__":
	main()
