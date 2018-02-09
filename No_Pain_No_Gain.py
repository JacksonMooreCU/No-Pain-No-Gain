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
		print(arena.area[0])
		print(0, window_wid)
		player.location = (random.randint(arena.area[0][0],arena.area[0][1]),random.randint(arena.area[1][0],arena.area[1][1]))
		
		print(">359",player.location)
		line.angle = 0
	

	# the points associated with each line segment must be recalculated as the angle changes
	line.segments = []
	
	# consider every line segment length
	for len in line.lengths:
	
		# compute the start of the line...
		sol_x = line.location[0] + math.cos(math.radians(line.angle)) * arena.radius * len[0]
		sol_y = line.location[1] + math.sin(math.radians(line.angle)) * arena.radius * len[0]
		
		# ...and the end of the line...
		eol_x = line.location[0] + math.cos(math.radians(line.angle)) * arena.radius * len[1]
		eol_y = line.location[1] + math.sin(math.radians(line.angle)) * arena.radius * len[1]
		
		# ...and then add that line to the list
		line.segments.append( ((sol_x, sol_y), (eol_x, eol_y)) )

	# start by assuming that no collisions have occurred
	player.collision = False
	
	# consider possible collisions between the circle hitbox and each line segment
	for seg in line.segments:
	
		# if there is any collision at all, the circle hitbox flag is set
		if detect_collision_line_circ(seg, (player.location, player.radius)):
			player.collision = True
			break

	# return the new state of the rotating line and the circle hitbox
	return line, player
	
#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def detect_collision_line_circ(u, v):

	# unpack u; a line is an ordered pair of points and a point is an ordered pair of co-ordinates
	(u_sol, u_eol) = u
	(u_sol_x, u_sol_y) = u_sol
	(u_eol_x, u_eol_y) = u_eol

	# unpack v; a circle is a center point and a radius (and a point is still an ordered pair of co-ordinates)
	(v_ctr, v_rad) = v
	(v_ctr_x, v_ctr_y) = v_ctr

	# the equation for all points on the line segment u can be considered u = u_sol + t * (u_eol - u_sol), for t in [0, 1]
	# the center of the circle and the nearest point on the line segment (that which we are trying to find) define a line 
	# that is is perpendicular to the line segment u (i.e., the dot product will be 0); in other words, it suffices to take
	# the equation v_ctr - (u_sol + t * (u_eol - u_sol)) · (u_evol - u_sol) and solve for t
	
	t = ((v_ctr_x - u_sol_x) * (u_eol_x - u_sol_x) + (v_ctr_y - u_sol_y) * (u_eol_y - u_sol_y)) / ((u_eol_x - u_sol_x) ** 2 + (u_eol_y - u_sol_y) ** 2)

	# this t can be used to find the nearest point w on the infinite line between u_sol and u_sol, but the line is not 
	# infinite so it is necessary to restrict t to a value in [0, 1]
	t = max(min(t, 1), 0)
	
	# so the nearest point on the line segment, w, is defined as
	w_x = u_sol_x + t * (u_eol_x - u_sol_x)
	w_y = u_sol_y + t * (u_eol_y - u_sol_y)
	
	# Euclidean distance squared between w and v_ctr
	d_sqr = (w_x - v_ctr_x) ** 2 + (w_y - v_ctr_y) ** 2
	
	# if the Euclidean distance squared is less than the radius squared
	if (d_sqr <= v_rad ** 2):
	
		# the line collides
		return True  # the point of collision is (int(w_x), int(w_y))
		
	else:
	
		# the line does not collide
		return False

	# visit http://ericleong.me/research/circle-line/ for a good supplementary resource on collision detection
	
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
	line = NPNG.Line([(arena.location),0,[(-1.00, -0.50),(-0.25, 0.25),(0.50, 1.00)],[]])
	'''
	rotating_line = {}
	rotating_line["ori"] = (arena.location)			# the "origin" around which the line rotates 
	rotating_line["ang"] = 0											# the current "angle" of the line
	rotating_line["len"] = [ (-1.00, -0.50),(-0.25, 0.25),(0.50, 1.00) ]# the "length" intervals that specify the gap(s)
	rotating_line["seg"] = [ ]											# the individual "segments" (i.e., non-gaps)
	'''
	
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
			if (start_button.clicked()):
				next_state = STATE_READY
			
		if (game_state == STATE_READY):
		
			closed_flag = quit()
		
		#####################################################################################################
		# this is the "update" phase of the game loop, where the changes to the game world are handled
		#####################################################################################################
		if (game_state == STATE_READY):
		
			line, player = main_game_update(arena,line, player) 
		
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
