import pygame
import maingame
import os
import time
import random

placeholder_graphic = pygame.image.load(os.getcwd()+"/res/player.png")
placeholder_graphic.set_colorkey(pygame.color.Color(255,255,255))

def get_rect_overlap(rect1, rect2):
     return (
        rect1.right-rect2.left if rect1.centerx<rect2.centerx else -(rect2.right - rect1.left),
        rect1.bottom-rect2.top if rect1.centery<rect2.centery else -(rect2.bottom - rect1.top),
        rect1,
        rect2
        )

def get_sign(number):
     return number/abs(number)

class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Entity(Point):
    """the basic superclass for game entities"""
    def __init__(self, x, y):
        super(Entity,self).__init__(x,y)
        self.velocity = Point(0,0)
        self.friction = 0
        self.size=Point(0,0)
        self.rect_offset = Point(0,0)
        self.facing = 0#down, right, up left
    
    def set_parent(self, parent):
        self.parent = parent
    
    def update(self, elapsed):
        #update position with velocity
        self.x+=self.velocity.x*elapsed
        self.y+=self.velocity.y*elapsed
        
        #momentum decay
        self.velocity.x = self.velocity.x*((1-self.friction)**elapsed)
        self.velocity.y = self.velocity.y*((1-self.friction)**elapsed)
        
        #binding to map limits
        self._map_bounds()
    
    def _map_bounds(self):
        if(self.x < 0):
            self.x = 0
            self.velocity.x = 0
        if(self.y < 0):
            self.y = 0
            self.velocity.y = 0
        if(self.x + self.size.x >= maingame.MAP_SIZE.x):
            self.x = maingame.MAP_SIZE.x - self.size.x - 1
            self.velocity.x = 0
        if(self.y >= maingame.MAP_SIZE.y):
            self.y = maingame.MAP_SIZE.y - 1
            self.velocity.y = 0
    
    def _get_tile(self):
        return self.parent.map_tiles[int(self.y/maingame.GRID_RESOLUTION)][int(round(self.x/maingame.GRID_RESOLUTION))]
    
    def _terrain_collision(self):
        selfrect = self.get_rect()
        for row in self.parent.map_tiles:
             for tile in row:
                  if(tile.raised and tile.get_rect().colliderect(selfrect)):
                    overlap = get_rect_overlap(tile.get_rect(), selfrect)
                    if(abs(overlap[0])<abs(overlap[1])):
                         self.x+=overlap[0]
                         self.velocity.x=0
                    else:
                         self.y+=overlap[1]
                         self.velocity.y=0
                    return
                
    
    def get_rect(self):
        return pygame.rect.Rect(self.x+self.rect_offset.x, self.y-self.size.y+self.rect_offset.y, self.size.x, self.size.y)
    
    def render(self,canvas):
        pass
   
    def post_render(self, canvas):
        pass
        

class LivingEntity(Entity):
    
    def __init__(self,x,y):
        super(LivingEntity, self).__init__(x,y)
        #TODO animation definitions
    
    def update(self,elapsed):
        super(LivingEntity, self).update(elapsed)
        self._terrain_collision()
    
    def render(self,canvas):
        #TODO frame selection from animation
        pass

class Player(LivingEntity):
    
    SPEED = 1000
    
    def __init__(self,x,y,color,
                 keybindings = {"LEFT": pygame.K_LEFT,
                                "RIGHT": pygame.K_RIGHT,
                                "UP": pygame.K_UP,
                                "DOWN": pygame.K_DOWN,
                                "PAINT": pygame.K_z,
                                "BOMB": pygame.K_x,
                                "ITEM": pygame.K_c}):
        super(Player,self).__init__(x,y)
        self.color = color
        self.keybindings = keybindings
        self.friction = 0.9
        self.size = Point(20,20)
        self.rect_offset = Point(15,10)
    
    def update(self,elapsed):
        super(Player,self).update(elapsed)
        
        if(self._pressed("LEFT")):
            self.velocity.x -= Player.SPEED * elapsed
        if(self._pressed("RIGHT")):
            self.velocity.x += Player.SPEED * elapsed
        if(self._pressed("UP")):
            self.velocity.y -= Player.SPEED * elapsed
        if(self._pressed("DOWN")):
            self.velocity.y += Player.SPEED * elapsed
        
        if(self._pressed("PAINT")):
            self._get_tile().paint_color = self.color
    
    def render(self,canvas):
        canvas.blit(placeholder_graphic,
                    (self.x - maingame.camerax,
                     self.y - maingame.cameray -
                         placeholder_graphic.get_size()[1])
                    )
    
    def _pressed(self,code):
        return pygame.key.get_pressed()[self.keybindings[code]]


class Police(LivingEntity):
     
     SPEED=100
     
     placeholder_police = pygame.image.load(os.getcwd()+"/res/police.png")
     placeholder_police.set_colorkey(pygame.color.Color(255,255,255))     
     policeimages = [
          placeholder_police.subsurface(pygame.rect.Rect(0,100,50,50)),
          placeholder_police.subsurface(pygame.rect.Rect(0,50,50,50)),
          placeholder_police.subsurface(pygame.rect.Rect(0,150,50,50)),
          placeholder_police.subsurface(pygame.rect.Rect(0,0,50,50)),
               ]
     
     path = []
     
     def __init__(self,x,y):
          super(Police, self).__init__(x,y)
          self.destination = None
          self.size = Point(20,20)
     
     def update(self, elapsed):
          self.velocity.y=0
          self.velocity.x=0
          if(self.destination is None):
               if(random.random()<0.2*elapsed):
                    self.facing = random.randint(0,3)
          else:
               if(self.destination == self._get_tile()):
                    self.destination = None
               else:
                    #print abs(self.x - self.path[0].gridx*maingame.GRID_RESOLUTION), abs(self.y - self.path[0].gridy*maingame.GRID_RESOLUTION), Police.SPEED
                    if(abs(self.x - self.path[0].gridx*maingame.GRID_RESOLUTION)<Police.SPEED*elapsed and
                       abs(self.y - (self.path[0].gridy+0.5)*maingame.GRID_RESOLUTION)<Police.SPEED*elapsed):
                         self.x = self.path[0].gridx*maingame.GRID_RESOLUTION
                         self.y = (self.path[0].gridy+0.5)*maingame.GRID_RESOLUTION
                         self.path = self.path[1:]
                    else:
                         if(self.x!=self.path[0].gridx*maingame.GRID_RESOLUTION):
                              self.velocity.x=Police.SPEED * get_sign(self.path[0].gridx*maingame.GRID_RESOLUTION-self.x)
                              self.facing = 1+2*(self.velocity.x<0)
                         else:
                              self.velocity.y=Police.SPEED * get_sign((self.path[0].gridy+0.5)*maingame.GRID_RESOLUTION-self.y)
                              self.facing = 0+2*(self.velocity.y<0)
          super(Police,self).update(elapsed)
                              
     
     def render(self,canvas):
          canvas.blit(Police.policeimages[self.facing],
                      (self.x - maingame.camerax,
                       self.y - maingame.cameray -
                           Police.policeimages[self.facing].get_size()[1])
                      )
     
     def alert_to(self,maptile):
          if(self.destination is not maptile):
               self.destination = maptile
               self.path = self.find_path(self._get_tile(),self.destination)#TODO pathfinding
               print self.path
          
     def find_path(self, current_tile, destination, path=[], cumscore=0):
          if current_tile == destination:
               return path+[current_tile]
          workingtiles=filter(lambda t: t.raised==False, current_tile.get_surrounding())
          
          for i in path:
               if i in workingtiles:
                    workingtiles.remove(i)
          
          for i in workingtiles:
               i.score = cumscore + i.manhattan(destination)
          workingtiles = sorted(workingtiles, key = lambda t: t.score)
          
          #print workingtiles
          
          for tile in workingtiles:
               if tile is destination:
                    return path+[current_tile, tile]
               else:
                    s = self.find_path(tile, destination, path+[current_tile], cumscore+tile.score)
                    if(s!=None):
                         return s
          return None
                    
           
          

class Camera(Entity):
     #seconds between rotations, in seconds
     rotation_time = 2
     rotation_order = [0,1,0,-1]#down right up left

     camera_sheet = pygame.image.load(os.getcwd()+"/res/camera.png")
     camera_sheet.set_colorkey(pygame.color.Color(255,255,255))
     cameraimages = [
          camera_sheet.subsurface(pygame.rect.Rect(0,50,50,50)),
          camera_sheet.subsurface(pygame.rect.Rect(0,100,50,50)),
          camera_sheet.subsurface(pygame.rect.Rect(0,150,50,50)),
          camera_sheet.subsurface(pygame.rect.Rect(0,0,50,50)),
          ]
     
     def __init__(self,x,y, police, initialtime = 0, rotation_modifer = 0):
          super(Camera, self).__init__(x,y)
          self.last_rotation = time.time()+ initialtime
          self.rotation_mod = rotation_modifer
          self.facing = random.randint(0,3)          
          self.police = police
          
          self.monitor_rects = [
               pygame.rect.Rect(self.x-1,self.y,50,150),
               pygame.rect.Rect(self.x-1,self.y,150,50),
               pygame.rect.Rect(self.x-1,self.y-100,50,150),
               pygame.rect.Rect(self.x-101,self.y,150,50)
               ]
     
     def update(self,elapsed):
          if(time.time() - self.last_rotation > Camera.rotation_time + self.rotation_mod):
               self.facing  = (self.facing+1)%4
               self.last_rotation = time.time()
               
     
     def render(self,canvas):
          canvas.blit(Camera.cameraimages[self.facing],
                                (self.x - maingame.camerax,
                                 self.y - maingame.cameray -
                                 Camera.cameraimages[self.facing].get_size()[1]))
          
     
     def post_render(self,canvas):
          pygame.draw.rect(canvas,
                           pygame.color.Color(255,0,0,50),
                           self.get_vision_rect().copy()
                           .move(- maingame.camerax, - maingame.cameray),
                           1)
     
     def get_vision_rect(self):
          return self.monitor_rects[self.facing]