#No Pain No Gain Screen Classes
import entitys
import pygame

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