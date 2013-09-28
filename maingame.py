from gameview import GameView
from maptile import MapTile
from random import randint
import pygame
import entities
from entities import Point
import random


GRID_RESOLUTION = 50
MAP_GRID_SIZE = Point(13,13)
MAP_SIZE = Point(MAP_GRID_SIZE.x * GRID_RESOLUTION,
                 MAP_GRID_SIZE.y * GRID_RESOLUTION)
camerax = -20
cameray = -40

class MainGame(GameView):
    """The main game class"""    
    
    def __init__(self,canvas):
        super(MainGame, self).__init__(canvas)
        
        self.map_tiles = self._make_map()
        self.entities = []
        self.cameras = []
        self.players = []
        self.police = []
        self._populate_map()
        
    def main_loop(self, elapsed):
        """moves forward the game"""
        for entity in self.entities:
            entity.update(elapsed)
        #TODO map behaviors
        for camera in self.cameras:
            for player in self.players:
                if(camera.get_vision_rect().colliderect(player.get_rect())):
                    closest = self.police[0]
                    for i in self.police:
                        if(i._get_tile().manhattan(player._get_tile())<closest._get_tile().manhattan(player._get_tile())):
                            closest=i
                    closest.alert_to(player._get_tile())
        """
        for police in self.police:
            for player in self.players:
                if(police.get_vision_rect().colliderect(player.get_rect())):
                    police.alert_to(player._get_tile)
        """
        
    def render(self):
        for row_number in range(len(self.map_tiles)):
            for tile in self.map_tiles[row_number]:
                tile.render(self.canvas)
            
            for entity in self.entities:
                if( int((entity.y-1)/GRID_RESOLUTION) ==  row_number):
                    entity.render(self.canvas)
        
        for entity in self.entities:
            entity.post_render(self.canvas)
    
    #begin helper functions
    def add(self, entity):
        entity.set_parent(self)
        self.entities.append(entity)
        
        if(isinstance(entity, entities.Camera)):
            self.cameras.append(entity)
        if(isinstance(entity, entities.Player)):
            self.players.append(entity)
        if(isinstance(entity, entities.Police)):
            self.police.append(entity)        
    
        return entity
    
    #begin construction functions
    def _make_map(self):
        retmap = []
        for y in range(MAP_GRID_SIZE.y):
            retmap.append([])
            for x in range(MAP_GRID_SIZE.x):
                raised = (x == 0 or
                          y == 0 or
                          x == (MAP_GRID_SIZE.x-1) or
                          y == (MAP_GRID_SIZE.y-1) or
                          (x%2 == 0 and y%2 == 0) or
                          ((x)%3 == 0 and (y)%3 == 0)
                          )
                retmap[y].append(MapTile(x,y,raised))
        
        for y in range(len(retmap)):
            for x in range(len(retmap)):
                if(x!=0):
                    retmap[y][x].neighbor_left = retmap[y][x-1]
                if(x!=len(retmap[y])-1):
                    retmap[y][x].neighbor_right = retmap[y][x+1]
                if(y!=0):
                    retmap[y][x].neighbor_up = retmap[y-1][x]
                if(y!=len(retmap)-1):
                    retmap[y][x].neighbor_down = retmap[y+1][x]
            
        return retmap
    
    def _populate_map(self):
        self.add(entities.Player(GRID_RESOLUTION,GRID_RESOLUTION*2,
                                          pygame.color.Color(23,71,166,255)
                                          ))
        
        pol = self.add(entities.Police(GRID_RESOLUTION*5,
                                 GRID_RESOLUTION*6+1)
                )        
        self.add(entities.Camera(GRID_RESOLUTION*3,
                                 GRID_RESOLUTION*3+1,
                                 random.random(),
                                 random.random())
                 )
        
        pol = self.add(entities.Police(GRID_RESOLUTION*7,
                                 GRID_RESOLUTION*6+1)
                )        
        self.add(entities.Camera(GRID_RESOLUTION*3,
                                 GRID_RESOLUTION*9+1,
                                 random.random(),
                                 random.random())
                 )
        
        pol = self.add(entities.Police(GRID_RESOLUTION*7,
                                 GRID_RESOLUTION*8+1)
                )        
        self.add(entities.Camera(GRID_RESOLUTION*9,
                                 GRID_RESOLUTION*9+1,
                                 random.random(),
                                 random.random())
                 )
        
        pol = self.add(entities.Police(GRID_RESOLUTION*5,
                                 GRID_RESOLUTION*8+1)
                )        
        self.add(entities.Camera(GRID_RESOLUTION*9,
                                 GRID_RESOLUTION*3+1,
                                 random.random(),
                                 random.random())
                 )