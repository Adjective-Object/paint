import pygame
import time
import sys
from maingame import MainGame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FRAMERATE_CAP = 60

BACKGROUND_FILL = pygame.color.Color(255, 255, 255, 255)

def do_game():
    pygame.init()
    
    screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paints!")
    maingame = MainGame(screen_surface)
    
    lastUpdate = time.time()
    
    while True:#main loop
        #check to see if close button has been pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        newUpdate = time.time()
        #update game loop
        maingame.main_loop(newUpdate-lastUpdate)
        #update image
        screen_surface.fill(BACKGROUND_FILL)
        maingame.render()
        #delay blitting so that framerate is kept under FRAMERATE_CAP
        if(newUpdate-lastUpdate < 1 / FRAMERATE_CAP):
            time.sleep(1/FRAMERATE_CAP-newUpdate-lastUpdate)
        lastUpdate = newUpdate
        #flip the display (show changes)
        pygame.display.flip()

        
if __name__ == "__main__":
    do_game()