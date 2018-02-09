from abc import ABC, abstractmethod
import pygame
import math
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
		self.speed = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10]
		self.speed_level = 4
		self.health = 100
		self.velocity = None
		
	def render (self, window_sfc):
	
		if self.collision:
		
			pygame.draw.circle(window_sfc, (255, 0, 0), self.location, self.radius)
		
		else:
			
			pygame.draw.circle(window_sfc, (255, 255, 255), self.location, self.radius)
			
		stats = "Health: "+str(self.health)+" Speed: "+str(self.speed_level)
				
			
		myfont = pygame.font.SysFont('Impact', 30)
		textsurface = myfont.render(stats, False, (0, 0, 255))
		window_sfc.blit(textsurface,(100, 50))
			
	def check_moving (self, arena):
		if (arena.clicked()[0]):
			self.destination = arena.clicked()[1]
			pos = self.location
			target = self.destination
			self.velocity = ((target[0]-pos[0])*self.speed[self.speed_level],(target[1]-pos[1])*self.speed[self.speed_level])
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
		self.damage = data[4]
	
	def render (self, window_sfc):
		# draw each of the rotating line segments
		for seg in self.segments:
	
			pygame.draw.aaline(window_sfc, (255, 255, 255), seg[0], seg[1])
			
	def compute_line (self, arena):
	
		# the points associated with each line segment must be recalculated as the angle changes
		self.segments = []
		
		# consider every line segment length
		for len in self.lengths:

			# compute the start of the line...
			sol_x = self.location[0] + math.cos(math.radians(self.angle)) * arena.radius * len[0]
			sol_y = self.location[1] + math.sin(math.radians(self.angle)) * arena.radius * len[0]
			
			# ...and the end of the self...
			eol_x = self.location[0] + math.cos(math.radians(self.angle)) * arena.radius * len[1]
			eol_y = self.location[1] + math.sin(math.radians(self.angle)) * arena.radius * len[1]
			
			# ...and then add that line to the list
			self.segments.append( ((sol_x, sol_y), (eol_x, eol_y)) )
			
	def check_collision (self,player):
	
		# start by assuming that no collisions have occurred
		player.collision = False
	
		# consider possible collisions between the circle hitbox and each line segment
		for seg in self.segments:
		
			# if there is any collision at all, the circle hitbox flag is set
			if self.detect_collision_line_circ(seg, (player.location, player.radius)):
				player.health -= self.damage
				player.collision = True
				break
			
	def detect_collision_line_circ(self, u, v):

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