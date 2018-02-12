#No Pain No Gain Screen Classes
import entitys
import pygame
from pygame.locals import *

class Screen :

	def __init__(self,data):
		self.type = data[0]
		self.button = data[1]
		self.text = data[2]
		self.view = data[3]
		self.next_screen = data[4]
		
	def render (self, window_sfc):
		print("render")
		# clear the window surface (by filling it with black)
		window_sfc.fill( (255,0,0) )
	
		myfont = pygame.font.SysFont('Impact', 30)
		textsurface = myfont.render(self.text, False, (0, 0, 255))
		window_sfc.blit(textsurface,(100, 50))
		
		self.button.render(window_sfc)
		
	def check_button (self):
		if (self.button.clicked()[0]):
			return True
		else:
			return False
			
	def quit(self):

		# look in the event queue for the quit event
		quit_ocrd = False
		for event in pygame.event.get():
			if event.type == QUIT:
				quit_ocrd = True
			
			if event.type == pygame.KEYDOWN:
				if(pygame.K_ESCAPE == event.key):
					quit_ocrd = True
			
		return quit_ocrd
			
class Battle (Screen):

	def __init__(self,data):
		self.type = "battle"
		self.arena = data[1]
		self.lines = data[2]
		self.goal = data[3]
		self.sprite = None
		
	def render(self,player,window_sfc):
		# clear the window surface (by filling it with black)
		window_sfc.fill( (0,0,0) )
	
		self.arena.render(window_sfc)
	
		for line in self.lines:
			line.render(window_sfc)
	
		self.goal.render(window_sfc)
	
		player.render(window_sfc)
	
	def update(self,player):
	
		for line in self.lines:
			# increase the angle of the rotating line
			line.move_line()

			# the rotating line angle ranges between 90 and 180 degrees
			if line.angle > 179:

				# when it reaches an angle of 180 degrees, reposition the circular hitbox
				
				##player.location = (random.randint(arena.area[0][0],arena.area[0][1]),random.randint(arena.area[1][0],arena.area[1][1]))
				self.goal.new(self.arena)
				line.angle = 0
			
			# consider every line segment length
			line.compute(self.arena)
			
			# consider possible collisions between the circle hitbox and each line segment
			line.check_collision(player)
		
		#check if player got a point
		player.check_goal(self.goal,self.arena)

		player.move(self.arena)
		# return the new state of the rotating line and the circle hitbox
		#return line, player, goal