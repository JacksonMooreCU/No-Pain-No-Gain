#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

import screens
import entitys
import pygame
import random
import math
import time

from pygame.locals import *
pygame.font.init()	# you have to call this at the start, 
					# if you want to use this module.

# the window is the actual window onto which the camera view is resized and blitted
window_wid = 1200
window_hgt = 600

# the frame rate is the number of frames per second that will be displayed and although
# we could (and should) measure the amount of time elapsed, for the sake of simplicity
# we will make the (not unreasonable) assumption that this "delta time" is always 1/fps
frame_rate = 30
delta_time = 1 / frame_rate


# constants for designating the different games states
STATE_TITLE = 0
STATE_CUTSCENE = 1
STATE_ROOM = 2
STATE_GAME = 3
STATE_STORE = 4
STATE_WIN = 100
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
	
	continue_button = entitys.Button([(window_sfc.get_width()/2-50,window_sfc.get_height()/2-50),(100,100)])
	cutscene = screens.Screen(["cutscene",continue_button,"No Input",None,1])
	
	battle_button = entitys.Button([(window_sfc.get_width()/2-250,window_sfc.get_height()/2-50),(100,100)])
	train_button = entitys.Button([(window_sfc.get_width()/2-50,window_sfc.get_height()/2-50),(100,100)])
	sleep_button = entitys.Button([(window_sfc.get_width()/2+150,window_sfc.get_height()/2-50),(100,100)])
	room = screens.Room(["room",[battle_button,train_button,sleep_button],"Battle, Train, or Rest?",[3,3,4]])

	speed_button = entitys.Button([(window_sfc.get_width()/2-200,window_sfc.get_height()/2-50),(100,100)])
	health_button = entitys.Button([(window_sfc.get_width()/2,window_sfc.get_height()/2-50),(100,100)])
	max_health_button = entitys.Button([(window_sfc.get_width()/2+200,window_sfc.get_height()/2-50),(100,100)])
	back_button = entitys.Button([(window_sfc.get_width()/2-550,window_sfc.get_height()/2-250),(50,50)])
	store = screens.Store(["store",[speed_button,health_button,max_health_button,back_button],"Speed, Health, or Max Health?",[4,4,4,2]])
	
	arena0 = entitys.Arena([(250),((window_wid // 2), (window_hgt // 2)),4,0])
	line0a = entitys.Line([(arena0.location),0,180,[(-1.00, -0.50),(-0.30, 0.30),(0.50, 1.00)],[],1,0])
	goal0 = entitys.Goal([(arena0.location),10,False,1],arena0)
	battle0 = screens.Battle(["battle",arena0,[line0a],goal0])
	
	arena1 = entitys.Arena([(250),((window_wid // 2), (window_hgt // 2)-50),4,1])
	line1a = entitys.Line([(arena1.location),0,180,[(-1.00, -0.50),(-0.30, 0.30),(0.50, 1.00)],[],1,1])
	goal1 = entitys.Goal([(arena1.location),10,False,1],arena1)
	battle1 = screens.Battle(["battle",arena1,[line1a],goal1])
	
	arena2 = entitys.Arena([(250),((window_wid // 2), (window_hgt // 2)-50),10,2])
	line2a = entitys.Line([(arena2.location),0,180,[(-1.00, -0.50),(-0.30, 0.30),(0.50, 1.00)],[],1,1])
	line2b = entitys.Line([(arena2.location),0,180,[(-1.00, -0.50),(-0.30, 0.30),(0.50, 1.00)],[],1,-1])
	goal2 = entitys.Goal([(arena2.location),10,False,2],arena2)
	battle2 = screens.Battle(["battle",arena2,[line2a,line2b],goal2])
	
	arena3 = entitys.Arena([(250),((window_wid // 2), (window_hgt // 2)-50),15,4])
	line3a = entitys.Line([(arena3.location),0,180,[(-1.00, -0.50),(-0.30, 0.30),(0.50, 1.00)],[],2,2])
	line3b = entitys.Line([(arena3.location),0,360,[(-1.00, -0.70),(-0.50, 0.50),(0.70, 1.00)],[],2,-2])
	goal3 = entitys.Goal([(arena3.location),10,False,3],arena3)
	battle3 = screens.Battle(["battle",arena3,[line3a,line3b],goal3])
	
	arena4 = entitys.Arena([(250),((window_wid // 2), (window_hgt // 2)-50),20,8])
	line4a = entitys.Line([(arena4.location),0,120,[(0, 0.4),(0.6, 1.00)],[],2,2])
	line4b = entitys.Line([(arena4.location),120,240,[(0, 0.4),(0.6, 1.00)],[],2,2])
	line4c = entitys.Line([(arena4.location),240,360,[(0, 0.4),(0.6, 1.00)],[],2,2])
	line4d = entitys.Line([(arena4.location),0,120,[(0, 0.4),(0.6, 1.00)],[],2,-2])
	line4e = entitys.Line([(arena4.location),120,240,[(0, 0.4),(0.6, 1.00)],[],2,-2])
	line4f = entitys.Line([(arena4.location),240,360,[(0, 0.4),(0.6, 1.00)],[],2,-2])
	goal4 = entitys.Goal([(arena4.location),10,False,4],arena4)
	battle4 = screens.Battle(["battle",arena4,[line4a,line4b,line4c,line4d,line4e,line4f],goal4])

	battles = [battle0,battle1,battle2,battle3,battle4]
	
	# this game object is a circular
	player = entitys.Player([((window_wid / 2), (window_hgt / 2)+100)])
	
	game_state = next_state
	
	# the game loop is a postcondition loop controlled using a Boolean flag
	closed_flag = False
	while not closed_flag:

			
		#####################################################################################################
		# this is the "inputs" phase of the game loop, where player input is retrieved and stored
		#####################################################################################################
		if (game_state == STATE_TITLE):
			time.sleep(0.1)
			closed_flag = title.quit()
			if (title.check_button()):
				next_state = STATE_ROOM
			
		elif (game_state == STATE_GAME):
		
			player.check_moving(battles[player.level].arena)
			closed_flag = battles[player.level].quit()
		
			
		elif (game_state == STATE_CUTSCENE):
		
			if(cutscene.check_button()):
				next_state = cutscene.next_screen
				
			closed_flag = cutscene.quit()
			
		elif (game_state == STATE_ROOM):
		
			if(room.check_buttons(player)):
				next_state = room.next_screen
			closed_flag = room.quit()
		
		elif (game_state == STATE_STORE):
		
			if(store.check_buttons(player)):
				next_state = store.next_screen
			closed_flag = room.quit()
			
		#####################################################################################################
		# this is the "update" phase of the game loop, where the changes to the game world are handled
		#####################################################################################################
		if (game_state == STATE_GAME):
	
			battles[player.level].update(player)
			
			#check if the player won
			if (battles[player.level].check(player,cutscene)):
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
			
		elif (game_state == STATE_STORE):
		
			store.render(player,window_sfc)
			
		elif (game_state == STATE_GAME):
		
			battles[player.level].render(player,window_sfc)
			
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
