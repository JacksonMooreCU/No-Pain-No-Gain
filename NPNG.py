from abc import ABC, abstractmethod
import pygame
#No Pain No Gain Class Files

class Entity :

	def __init__(self,data):
		self.type = data[0]
		self.location = data[1]
		self.size = data[2]
		
	def clicked(self):
		(mouseX, mouseY) = pygame.mouse.get_pos()
		if(mouseX<self.location[0]+self.size[0] and mouseX>self.location[0] and mouseY<self.location[1]+self.size[1] and mouseY>self.location[1] and pygame.mouse.get_pressed()[0]):
			
			return True
	
class Button(Entity):

	def __init__(self, data):
		self.type = "button"
		self.location = data[0]
		self.size = data[1]
	
	def render(self, window_sfc):
		pygame.draw.rect(window_sfc, (0, 0, 0), (window_sfc.get_width()/2-50,window_sfc.get_height()/2-50)+(100,100), 0)
		
class Arena(Entity):

	def __init__(self, data):
		self.type = "arena"
		self.radius = data[0]
		self.diameter = data[0] * 2
		self.location = data[1]
		self.size = (data[0] * 2,data[0] * 2)
		self.area = (((self.location[0] - self.radius),(self.location[0] + self.radius)),((self.location[1] - self.radius),(self.location[1] + self.radius)))
		
	def render(self, window_sfc):	
		pygame.draw.circle(window_sfc, (0, 255, 0), self.location, self.radius)
		
class Player (Entity):
	
	def __init__(self, data):
		self.type = "player"
		self.location = data[0]
		self.radius = data[1]
		self.collision = data[2]
		self.size = (data[0] * 2,data[0] * 2)
		
	def render (self, window_sfc):
	
		if self.collision:
		
			pygame.draw.circle(window_sfc, (255, 0, 0), self.location, self.radius)
		
		else:
			
			pygame.draw.circle(window_sfc, (255, 255, 255), self.location, self.radius)
		
class Line (Entity):
	
	def __init__(self, data):
		self.type = "line"
		self.location = data[0]
		self.angle = data[1]
		self.lengths = data[2]
		self.segments = data[3]
	
	def render (self, window_sfc):
		# draw each of the rotating line segments
		for seg in self.segments:
	
			pygame.draw.aaline(window_sfc, (255, 255, 255), seg[0], seg[1])