import pygame
import os
import sys
from gameview import GameView

class AboutScreen(GameView):
    
    splash = pygame.image.load(os.getcwd()+"/res/menu/about_splash.png")
    
    def __init__(self, canvas):
        super(AboutScreen, self).__init__(canvas)
        self.exit=False
    
    def render(self):
        self.canvas.blit(AboutScreen.splash, (0,0))
    
    def main_loop(self, elapsed):
        keys=pygame.key.get_pressed()
        self.exit = keys[pygame.K_ESCAPE]