from maptile import MapTile
           
class Zone(object):
    
    paint_blocks = 0.00
    
    def __init__(self):
        x1 = [None, None, None, None]
        x2 = [None, None, None, None]
        x3 = [None, None, None, None]
        x4 = [None, None, None, None]
        zone = [x1, x2, x3, x4]
        
    def add(self, mp):
        """
        Adds a maptile to the zone, added from top left to bottom right.
        If the maptile isnt raised it adds a number to paint_blocks for
        zone control calculations
        """
        
        for i, j in product(range(4), repeat = 2):
            if(self.zone[i][j] == None):
                self.zone[i][j] = mp
                if(self.zone[i][j].raised == False):
                    self.paint_blocks += 1.00
                return
                
        print("Nothing done, mate.")
    
    
    def replace(self, x, y, mp):
        self.zone[x][y] = mp
        
        
    def set_player_number(self, x, y, number):
        self.zone[x][y] = number
        
        
    def get_player_number(self, x, y):
        return self.zone[x][y].player_number
    
    
    def get_owner(self, n):
        """ 
        Returns the player_number of whoever has control
        over the zone, requires at least 51%
        Takes an int n for the number of players in the game, works with
        numbers greater than but less efficient.
        """ 
        for i in range(n):
            if(get_percent(n) >= .51):
                return n
            
        return 0
    
    
    def get_percent(self, n):
        """
        Returns percent control of player n
        """
        controlled = 0.00
        for i, j in product(range(4), repeat = 2):
            if(self.zone[i][j].player_number == n):
                controlled += 1.00
        
        return float(controlled / self.paint_blocks)