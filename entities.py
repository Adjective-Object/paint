import pygame
class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Entity(Point):
    """the basic superclass for game entities"""
    def __init__(self, x, y):
        super(Entity,self).__init(x,y)
        self.velocity = Point(0,0)
        self.friction = 0.1
    
    def update(self, elapsed):
        #update position with velocity
        self.x+=self.velocity.x*elapsed
        self.y+=self.velocity.y*elapsed
        
        #momentum decay
        self.velocity.x = self.velocity.x*((1-self.friction)**elapsed)
        self.velocity.y = self.velocity.y*((1-self.friction)**elapsed)
    
    def render(self,canvas):
        pass

class LivingEntity(Entity):
    
    def __init__(self,x,y):
        super(LivingEntity, self).__init__(x,y)
        #TODO animation definitions
    
    def update(self,elapsed):
        super(LivingEntity, self).update(elapsed)
    
    def render(self,canvas):
        #TODO frame selection from animation
        pass

class Player(Entity):
    
    SPEED = 10
    
    def __init__(self,x,y,
                 keybindings = {"LEFT": pygame.K_LEFT,
                                "RIGHT": pygame.K_RIGHT,
                                "UP": pygame.K_UP,
                                "DOWN": pygame.K_DOWN,
                                "PAINT": pygame.K_Z,
                                "BOMB": pygame.K_X,
                                "ITEM": pygame.K_C}):
        super(Player,self).__init__(x,y)
        
        self.keybindings = keybindings    
    
    def update(self,elapsed):
        super(Player,self).update(elapsed)
        
        if(self._pressed("LEFT")):
            self.velocity.x -= 10 * elapsed
        if(self._pressed("RIGHT")):
            self.velocity.x += 10 * elapsed
        if(self._pressed("UP")):
            self.velocity.y -= 10 * elapsed
        if(self._pressed("DOWN")):
            self.velocity.y += 10 * elapsed
    
    def _pressed(self,code):
        return pygame.key.get_pressed()[keybindings[code]]