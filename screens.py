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
				print("quit")
				quit_ocrd = True
			
			if event.type == pygame.KEYDOWN:
				if(pygame.K_ESCAPE == event.key):
					print("quit")
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
			if line.angle > line.rotation:

				# when it reaches an angle of 180 degrees, reposition the circular hitbox
				
				##player.location = (random.randint(arena.area[0][0],arena.area[0][1]),random.randint(arena.area[1][0],arena.area[1][1]))
				self.goal.new(self.arena)
				line.angle = line.origin
			
			# consider every line segment length
			line.compute(self.arena)
			
			# consider possible collisions between the circle hitbox and each line segment
			line.check_collision(player)
		
		#check if player got a point
		player.check_goal(self.goal,self.arena)

		player.move(self.arena)
		# return the new state of the rotating line and the circle hitbox
		#return line, player, goal
		
	def check(self,player,cutscene):
	
		#if the player has enough points for the arena they are in
		if(player.points >= self.arena.score):
			player.points = 0; 			# reset the players points
			cutscene.text = "You win!" #In the cutscene show that the player won
			if (player.training_mode):
				cutscene.text += " You gained"+str(self.arena.score)+"points!"
				player.money += self.arena.score
			else:
				cutscene.text += " You gained 1 rank!"
				player.rank -= 1
				player.level += 1
			cutscene.next_screen = 2 #then go to the room
			#reset variables
			player.destination = None
			player.velocity = None
			player.moving = False
			player.location = (self.arena.location[0],self.arena.location[1]+(self.arena.radius//2))
			player.int_location = (self.arena.location[0],self.arena.location[1]+(self.arena.radius//2))
			for line in self.lines:
				line.angle = line.origin
			return True #return true for the battle is over
		#if the player has no more health left
		elif(player.health <= 0):
			cutscene.text = "You lose!"#in the cutscene show that the player lost
			cutscene.next_screen = 99 #re run the game
			return True#return true for the battle is over
		else:
			return False#return false since the battle is not over
		
class Room (Screen):

	def __init__(self,data):
		self.type = data[0]
		self.buttons = data[1]
		self.text = data[2]
		self.next_screens = data[3]
		self.clicked = None
		self.next_screen = None
		
	def render (self,player, window_sfc):
	
		# clear the window surface (by filling it with black)
		window_sfc.fill( (255,0,0) )
		
		myfont = pygame.font.SysFont('Impact', 30)
		self.text = "Battle, Train, or Rest? HP: "+str(player.health)+" Days: "+str(player.days)+" Rank: "+str(player.rank)+" Money: "+str(player.money)
		textsurface = myfont.render(self.text, False, (0, 0, 255))
		window_sfc.blit(textsurface,(100, 50))
		
		for button in self.buttons:
			button.render(window_sfc)
			
	def check_buttons(self,player):
		
		for x in range(len(self.buttons)):
		
			if (self.buttons[x].clicked()[0]):
			
				self.clicked = x
				self.next_screen = self.next_screens[self.clicked]
				if(x==1): 
					player.training_mode=True
					player.days += 1
				elif(x==0): 
					player.training_mode=False
					player.days += 1
					
				return True
				
		return False
		
class Store (Screen):

	def __init__(self,data):
		self.type = data[0]
		self.buttons = data[1]
		self.text = data[2]
		self.next_screens = data[3]
		self.clicked = None
		self.next_screen = None
		
	def render (self,player, window_sfc):
	
		# clear the window surface (by filling it with black)
		window_sfc.fill( (255,0,0) )
		
		myfont = pygame.font.SysFont('Impact', 30)
		self.text = "Increase speed, health, max health? Speed: "+str(player.speed_level)+" Health: "+str(player.health)+" Max Health: "+str(player.health_levels[player.health_level])
		textsurface = myfont.render(self.text, False, (0, 0, 255))
		window_sfc.blit(textsurface,(100, 50))
		self.text = "Cost of speed, health, max health? Speed: "+str(player.speed_cost[player.speed_level])+" Health: "+str(player.health_cost)+" Max Health: "+str(player.max_health_cost[player.health_level])+" Money: "+str(player.money)
		textsurface = myfont.render(self.text, False, (0, 0, 255))
		window_sfc.blit(textsurface,(100, 100))
		
		for button in self.buttons:
			button.render(window_sfc)
			
	def check_buttons(self,player):
		
		for x in range(len(self.buttons)):
		
			if (self.buttons[x].clicked()[0]):
			
				self.clicked = x
				self.next_screen = self.next_screens[self.clicked]
				if(x==0 and player.money>=player.speed_cost[player.speed_level]): 
					player.money -= player.speed_cost[player.speed_level]
					player.speed_level+= 1
					
				if(x==1 and player.money>=player.max_health_cost[player.health_level]): 
					player.money -= player.max_health_cost[player.health_level]
					player.health_level+= 1
					
				if(x==1 and player.money>=player.health_cost and player.health<100): 
					player.money -= player.health_cost
					player.health+= 1
				return True
				
		return False