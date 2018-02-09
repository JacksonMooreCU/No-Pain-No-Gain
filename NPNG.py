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
			
			return True, (mouseX, mouseY)
		else:	
			return False, (mouseX, mouseY)
	
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
	
	def clicked(self):
		(mouseX, mouseY) = pygame.mouse.get_pos()
		if(mouseX<self.location[0]+self.radius and mouseX>self.location[0]-self.radius and mouseY<self.location[1]+self.radius and mouseY>self.location[1]-self.radius and pygame.mouse.get_pressed()[0]):
			
			return True, (mouseX, mouseY)
		else:	
			return False, (mouseX, mouseY)
	
	def render(self, window_sfc):	
		pygame.draw.circle(window_sfc, (0, 255, 0), self.location, self.radius)
		
class Player (Entity):
	
	def __init__(self, data):
		self.type = "player"
		self.location = data[0]
		self.radius = data[1]
		self.collision = data[2]
		self.size = (data[0] * 2,data[0] * 2)
		self.destination = data[0]
		self.moving = False
		self.speed = 1
		self.velocity = None
		
	def render (self, window_sfc):
	
		if self.collision:
		
			pygame.draw.circle(window_sfc, (255, 0, 0), self.location, self.radius)
		
		else:
			
			pygame.draw.circle(window_sfc, (255, 255, 255), self.location, self.radius)
			
	def check_moving (self, arena):
		if (arena.clicked()[0]):
			self.destination = arena.clicked()[1]
			pos = self.location
			target = self.destination
			self.velocity = ((target[0]-pos[0])*0.05,(target[1]-pos[1])*0.05)
			self.moving = True
			
			
	def move(self,arena):
		perimeter = arena.location
		pos = list(self.location)
		if (self.moving):
		
			target = pos[0]<self.destination[0]+10 and pos[0]>self.destination[0]-10 and pos[1]<self.destination[1]+10 and pos[1]>self.destination[1]-10
			bounds = pos[0]<perimeter[0]+arena.radius and pos[0]>perimeter[0]-arena.radius and pos[1]<perimeter[1]+arena.radius and pos[1]>perimeter[1]-arena.radius
		
		
			if(bounds and not target):
				pos[0] += self.velocity[0]
				pos[1] += self.velocity[1]
				print("loc: ",self.location,"des:",self.destination,"target:",target,"vel0:",self.velocity[0],"vel1:",self.velocity[1])
				print(pos[0]<self.destination[0]+50 , pos[0]>self.destination[0]-50 ,pos[1]<self.destination[1]+50 , pos[1]>self.destination[1]-50)
				self.location = (int(pos[0]),int(pos[1]))
				
			else:
				self.destination = None
				self.velocity = None
				self.moving = False
			
		
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