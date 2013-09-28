import os
import pygame
import maingame

#for some reason I have to specify the directory with respect to root....
tile_raised = pygame.image.load(os.getcwd()+"/res/tile_raised.png")
tile_ground = pygame.image.load(os.getcwd()+"/res/tile.png")

mask_down = pygame.mask.from_surface(
    pygame.image.load(os.getcwd()+"/res/tile_down_mask.png"))
mask_up_front = pygame.mask.from_surface(
    pygame.image.load(os.getcwd()+"/res/tile_raised_mask_front.png"))
mask_up_left = pygame.mask.from_surface(
    pygame.image.load(os.getcwd()+"/res/tile_raised_mask_left.png"))
mask_up_right = pygame.mask.from_surface(
    pygame.image.load(os.getcwd()+"/res/tile_raised_mask_right.png"))

class MapTile(object):
    
    def __init__(self, x, y, parent, raised=False):
        self.paint_color = None
        self.raised = raised
        self.parent = parent
        
        self.gridx = x
        self.gridy = y
        
        self.neighbor_left = None
        self.neighbor_right = None
        self.neighbor_up = None
        self.neighbor_down = None
        
        self.score = 0#for pathfinding
        
    def get_neighbor(self, facing):
        if(facing == 0):
            return self.neighbor_down
        elif(facing == 1):
            return self.neighbor_right
        elif(facing == 2):
            return self.neighbor_up
        else:
            return self.neighbor_left
        
        
    def get_rect(self):
        return pygame.rect.Rect(self.gridx*maingame.GRID_RESOLUTION,
                                (self.gridy)*maingame.GRID_RESOLUTION,
                                maingame.GRID_RESOLUTION,
                                maingame.GRID_RESOLUTION)

    def get_surrounding(self, noWalls = False):
        surr =  [self.neighbor_down, self.neighbor_right,
                 self.neighbor_up, self.neighbor_left]
        while None in surr:
            surr.remove(None)
        if(noWalls):
            surr=filter(lambda t: t.raised==False, surr)
        return surr
    

    def manhattan(self, other):
        return abs(self.gridx-other.gridx)+abs(self.gridy-other.gridy)

    def render(self, canvas):
        image = tile_ground
        if(self.raised):
            image = tile_raised
        #TODO painted surfaces
        canvas.blit(image,
                    (self.gridx * maingame.GRID_RESOLUTION - 
                         self.parent.camerax ,
                     (self.gridy + 1) * maingame.GRID_RESOLUTION -
                         self.parent.cameray - image.get_size()[1])
                    )
        if(self.paint_color is not None):
            #TODO: masking images instead of tile tinting
            x = image.convert_alpha()
            self.paint_color.a = 80;
            x.fill(self.paint_color)
            canvas.blit(x,
                    (self.gridx * maingame.GRID_RESOLUTION - 
                         self.parent.camerax ,
                     (self.gridy + 1) * maingame.GRID_RESOLUTION -
                         self.parent.cameray - image.get_size()[1])
                    )
    def __repr__(self):
        return "[Tile %s,%s  %s]"%(self.gridx, self.gridy, self.score)
            
