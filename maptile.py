import os
import pygame
import maingame

#for some reason I have to specify the directory with respect to root....
tile_raised = pygame.image.load(os.getcwd()+"/res/tile_raised.png")
tile_ground = pygame.image.load(os.getcwd()+"/res/tile.png")

class MapTile(object):
    
    def __init__(self, x, y, raised=False):
        self.paint_color = pygame.color.Color(255,255,255)
        self.raised = raised
        
        self.gridx = x
        self.gridy = y
        
        self.neighbor_left = None
        self.neighbor_right = None
        self.neighbor_up = None
        self.neighbor_down = None

    def render(self, canvas):
        image = tile_ground
        if(self.raised):
            image = tile_raised
        canvas.blit(image,
                    (self.gridx * maingame.GRID_RESOLUTION - 
                         maingame.camerax ,
                     self.gridy * maingame.GRID_RESOLUTION -
                         maingame.cameray - image.get_size()[1])
                    )