from gameview import GameView
from maptile import MapTile
from random import randint

GRID_RESOLUTION = 48
camerax=100
cameray=100

class MainGame(GameView):
    """The main game class"""    
    
    def __init__(self,canvas):
        super(MainGame, self).__init__(canvas)
        
        self.map_tiles = sesslf._make_map()

    def main_loop(self, elapsed):
        """moves forward the game"""
    
    def render(self):
        for tile in self.map_tiles:
            tile.render(self.canvas)
        
    #begin construction functions
    
    def _make_map():
        map = []
        for x in range(10):
            map.append([])
            for y in range(10):
                map.append(MapTile(x,y,random.randint(0,1)))
    
    