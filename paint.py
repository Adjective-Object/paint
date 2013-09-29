import pygame
import time
import sys
import os
import sys
from about import AboutScreen
from maingame import MainGame
from mainmenugame import MainMenu

'''
PAINT WAR

The main game will run from this file. Do not be deceived my the module 'maingame.' 
This file will instantiate a maingame instance.

'''

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FRAMERATE_CAP = 60

BACKGROUND_FILL = pygame.color.Color(255, 255, 255, 255)

def do_game():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=16, channels=2, buffer=4096)
    
    screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paints")
    
    menu = MainMenu(screen_surface)
    about = AboutScreen(screen_surface)
    maingame = MainGame(screen_surface)
    
    #pygame.mixer.music.load(os.getcwd()+"/res/song.wav")
    #pygame.mixer.music.play(-1)    
    while True:
        menu.exitTo = None
        about.exit = False
        loop(screen_surface,
             lambda elapsed: menu.main_loop(elapsed),#main loop of game
             lambda : menu.render(),
             lambda t : menu.exitTo is None) #rendering it
        if(menu.exitTo == "2p"):
            #TODO this
            loop(screen_surface,
                 lambda elapsed: maingame.main_loop(elapsed),#main loop of game
                 lambda : maingame.render()) #rendering it
        if(menu.exitTo == "4p"):
            #TODO this
            loop(screen_surface,
                 lambda elapsed: maingame.main_loop(elapsed),#main loop of game
                 lambda : maingame.render()) #rendering it
        if(menu.exitTo == "about"):
            loop(screen_surface,
                 lambda elapsed: about.main_loop(elapsed),#main loop of about screen
                 lambda : about.render(),
                 lambda t : not about.exit) #rendering it       
    pygame.quit()
    sys.exit()
   
    

def loop(screen_surface, loopfn, dorender, loopcontrol=lambda initialTime: True ):
    initial = time.time()
    lastUpdate = initial
    while loopcontrol(initial):#main loop    
        #check to see if close button has been pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        newUpdate = time.time()
        #update game loop
        loopfn(newUpdate-lastUpdate)
        #update image
        screen_surface.fill(BACKGROUND_FILL)
        dorender()
        #delay blitting so that framerate is kept under FRAMERATE_CAP
        if(newUpdate-lastUpdate < 1 / FRAMERATE_CAP):
            time.sleep(1/FRAMERATE_CAP-newUpdate-lastUpdate)
        lastUpdate = newUpdate
        #flip the display (show changes)
        pygame.display.flip()        
        
if __name__ == "__main__":
    do_game()
    

