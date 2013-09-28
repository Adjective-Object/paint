from maptile import MapTile
           
class Zone(object):
    
    paint_blocks = 0.00
    player_number = 0
    raised = False
    
    def __init__(self):
        self.tile_contents = []
        
    def add(self, mp):
        """
        Adds a maptile to the zone
        If the maptile isnt raised it adds a number to paint_blocks for
        zone control calculations
        """
        
        self.tile_contents.append(mp)
        if(self.tile_contents[-1].raised == False):
            self.paint_blocks += 1.00
    
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
    
    def calculate_owner(self, n):
        """
        Updates player_number
        """
        self.player_number = self.get_owner(n)
    
    def get_dominant_color(self):
	colors = [None]
	frequencies = [0]
	
	for tile in self.tile_contents:
	    color = tile.paint_color
	    if color is not None:
		if not color in colors:
		    colors.append(color)
		    frequencies.append(1)
		else:
		    frequencies[colors.index(color)] += 1
	
	freqs = sorted(colors, key=lambda c: (frequencies[colors.index(c)]), reverse=True)
	if(len(freqs)>=2 and frequencies[colors.index(freqs[0])] == frequencies[colors.index(freqs[1])]):
	    return None
	return freqs[0]
    
    def get_percent(self, n):
        """
        Returns percent control of player n
        """
        controlled = 0.00
        for i in range(len(self.tile_contents)):
            if(self.tile_contents[i].player_number == n):
                controlled += 1.00
        
        return float(controlled / self.paint_blocks)

    def __repr__(self):
        return "[ZONE %s]"%(len(self.tile_contents))