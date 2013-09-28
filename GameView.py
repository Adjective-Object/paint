from threading import Thread


class GameView:
    """A state of the game. The menu can be a gameview, the game itself
       is another gameview. The point of this is to keep the resources and
       everything that may be necessary all contained.
       
       gameviews are given a canvas to work off of.
       The canvas is shared by gameviews, and is used so that the same
       window can display different things at different times
    """
    def __init__(self, canvas):
        """Initializes the gameview"""
        self.canvas = canvas
    
    def render(self):
        """renders the gameview to the canvas"""
        pass
    
    def mainThread(self):
        """the main thread of this GameView"""
    
    def start(self, elapsed):
        t = Thread(self.mainThread)
        t.start()