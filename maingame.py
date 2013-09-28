from gameview import GameView
from maptile import MapTile
from random import randint

GRID_RESOLUTION = 50
camerax=-100
cameray=-100

class MainGame(GameView):
    """The main game class"""    
    
    def __init__(self,canvas):
        super(MainGame, self).__init__(canvas)
        
        self.map_tiles = self._make_map()

    def main_loop(self, elapsed):
        """moves forward the game"""
    
    def render(self):
        for row_number in range(len(self.map_tiles)):
            for tile in self.map_tiles(row_number):
                tile.render(self.canvas)
            for entity in self.entities:
                if( int(entity.y) ==  row_number):
                    entity.render(self.canvas)
        
    #begin construction functions
    
    def _make_map(self):
        map = []
        for y in range(10):
            map.append([])
            for x in range(10):
                map[y].append(MapTile(x,y,randint(0,1)))
        return map