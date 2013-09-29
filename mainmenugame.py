import pygame
import os
import sys
from gameview import GameView

class MainMenu(GameView):
    
    
    splash = pygame.image.load(os.getcwd()+"/res/menu/splash.png")
    arrow = pygame.image.load(os.getcwd()+"/res/menu/arrow.png")
    game_2p = pygame.image.load(os.getcwd()+"/res/menu/2player.png")
    game_4p = pygame.image.load(os.getcwd()+"/res/menu/4player.png")
    about = pygame.image.load(os.getcwd()+"/res/menu/about.png")
    exit = pygame.image.load(os.getcwd()+"/res/menu/exit.png")
    
    def __init__(self, canvas):
        super(MainMenu, self).__init__(canvas)
        self.exitTo=None
        self.selected = 0
        self.buttons = [MainMenu.game_2p, MainMenu.game_4p,
                        MainMenu.about, MainMenu.exit]
        
        def game_2p():
            self.exitTo="2p"
    
        def game_4p():
            self.exitTo="4p"
        
        def about():
            self.exitTo="about"
        
        def killall():
            pygame.quit()
            sys.exit()
            
        self.options = [
            game_2p,
            game_4p,
            about,
            killall
            ]
    
        self.repeatable=True
    
    def render(self):
        self.canvas.blit(MainMenu.splash, (0,0))
        for i in range(len(self.buttons)):
            if(i==self.selected):
                self.canvas.blit(self.buttons[i],(140,400+i*90))
                self.canvas.blit(MainMenu.arrow,(100,400+i*90))
            else:
                self.canvas.blit(self.buttons[i],(100,400+i*90))
    
    def main_loop(self, elapsed):
        """the main loop of this GameView. Iterates the world by the
           elapsed number of seconds
        """
        key = pygame.key.get_pressed()
        if(self.repeatable):
            if(key[pygame.K_UP] or key[pygame.K_w]):
                self.selected = (self.selected-1)%len(self.buttons)
                self.repeatable=False
            if(key[pygame.K_DOWN] or key[pygame.K_s]):
                self.selected = (self.selected+1)%len(self.buttons)
                self.repeatable=False
            if(key[pygame.K_RETURN] or key[pygame.K_z]):
                self.options[self.selected]()
                self.repeatable=False
        
        elif not(key[pygame.K_UP] or key[pygame.K_w] or
                    key[pygame.K_DOWN] or key[pygame.K_s] or
                    key[pygame.K_RETURN] or key[pygame.K_z]):
            self.repeatable = True