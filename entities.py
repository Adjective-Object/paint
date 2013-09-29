import pygame
import maingame
import os
import time
import random

def get_rect_overlap(rect1, rect2):
     return (
        rect1.right-rect2.left if rect1.centerx<rect2.centerx else -(rect2.right - rect1.left),
        rect1.bottom-rect2.top if rect1.centery<rect2.centery else -(rect2.bottom - rect1.top),
        rect1,
        rect2
        )

def get_sign(number):
     return int(number/abs(number))

class Point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
     
    def __repr__(self):
        return "[Point %s, %s]"%(self.x, self.y)

class Entity(Point):
    """
    The basic superclass for game entities. 
    """
    def __init__(self, x, y):
        super(Entity,self).__init__(x,y)
        self.velocity = Point(0,0)
        self.friction = 0
        self.max_velocity = Point(9999,9999)
        self.size=Point(0,0)
        self.rect_offset = Point(0,0)
        # 0-down, 1-right, 2-up, 3-left
        self.facing = 0 
        self.collides_terrain = False
        self.alive=True
        self.stasis = 0
    
    def set_parent(self, parent):
        self.parent = parent

    def update(self, elapsed):
        #update position with velocity
        if(abs(self.velocity.x)>self.max_velocity.x):
             self.max_velocity.x*get_sign(self.velocity.x)
        if(abs(self.velocity.y)>self.max_velocity.y):
             self.max_velocity.y*get_sign(self.velocity.y)
          
          
          
             
        to_move = Point(self.velocity.x*elapsed, self.velocity.y*elapsed)
        
        #SUUPER inefficient way of colliding with terrain no matter what
        num_loops = 1
        if(self.collides_terrain):
             num_loops=int(max(abs(to_move.x), abs(to_move.y))/ 10 )+1
        #print to_move
        for i in range(num_loops):
             self.x+=1.0*to_move.x/num_loops
             self.y+=1.0*to_move.y/num_loops
             if(self.collides_terrain):                  
                  self._terrain_collision()                  
             self._map_bounds()
     
        if abs(self.velocity.x)<=self.friction*elapsed:
             self.velocity.x = 0
        else:
             self.velocity.x -= get_sign(self.velocity.x)*self.friction*elapsed
        if abs(self.velocity.y)<= self.friction*elapsed:
             self.velocity.y = 0
        else:
             self.velocity.y -= get_sign(self.velocity.y)*self.friction*elapsed
    
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
          for row in self.parent.map_tiles:
             for tile in row:
                  selfrect = self.get_rect()
                  if(tile.raised and tile.get_rect().colliderect(selfrect)):
                    overlap = get_rect_overlap(tile.get_rect(), selfrect)
                    if(abs(overlap[0])<=abs(overlap[1])):
                         self.x+=overlap[0]
                         self.velocity.x=0
                    if(abs(overlap[0])>=abs(overlap[1])):
                         self.y+=overlap[1]
                         self.velocity.y=0
          
    def get_rect(self):
          return pygame.rect.Rect(self.x+self.rect_offset.x, self.y-self.size.y+self.rect_offset.y, self.size.x, self.size.y)
    
    def render(self,canvas):
          pass
   
    def post_render(self, canvas):
          pass
        

class LivingEntity(Entity):
    
    def __init__(self,x,y):
        super(LivingEntity, self).__init__(x,y)
        self.collides_terrain = True
        #TODO animation definitions
    
    def update(self,elapsed):
        super(LivingEntity, self).update(elapsed)
    
    def render(self,canvas):
        #TODO frame selection from animation
        pass
   
    def look_at(self, destinationTile):
        dx = int(destinationTile.gridx*maingame.GRID_RESOLUTION)
        dy = int((destinationTile.gridy+0.5)*maingame.GRID_RESOLUTION)
        
        if(abs(self.x-dx)>5):
          self.facing = 1 + 2*get_sign(dx-self.x)
        elif (abs(self.y-dy)>10):
          self.facing = 2*get_sign(dy-self.y)   

class Player(LivingEntity):
     placeholder_graphic = pygame.image.load(os.getcwd()+"/res/player.png")
     placeholder_graphic.set_colorkey(pygame.color.Color(255,255,255)) 
     
     placeholders = [
           placeholder_graphic.subsurface(pygame.rect.Rect(0,0,50,50)),
           placeholder_graphic.subsurface(pygame.rect.Rect(0,50,50,50)),
           placeholder_graphic.subsurface(pygame.rect.Rect(0,100,50,50)),
           placeholder_graphic.subsurface(pygame.rect.Rect(0,150,50,50)),
     ]
     
     SPEED = 100
     MAX_SPEED = 350
     RAMPUP = 0.46
     BOMB_COOLDOWN = 5
     
     def __init__(self,x,y,n,color,
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
          self.max_speed = Point(Player.MAX_SPEED,Player.MAX_SPEED)
          self.size = Point(50,50)
          self.rect_offset = Point(0,0)
          self.bomb = True
          self.explosion = pygame.mixer.Sound(os.getcwd()+"/res/bomb_noise.wav")
          self.player_number = n
          self.bombcooldown = 0
          self.collides_terrain = True          
      
     def update(self,elapsed):
          super(Player,self).update(elapsed)
          
          #The player moves along the map grid tiles.
          if (self._pressed("LEFT")):
              self.x -= 50
              self.facing = 3
          elif (self._pressed("RIGHT")):
              self.x += 50
              self.facing = 1
          elif (self._pressed("UP")):
              self.y -= 50
              self.facing = 2
          elif (self._pressed("DOWN")):
              self.y += 50
              self.facing = 0
       
          if(self._pressed("PAINT")):
               if(self._get_tile().paint_color != self.color):
                  self._get_tile().paint_color = self.color
                  self._get_tile().player_number = self.player_number
          
          if(self._pressed("BOMB") and self.bombcooldown<=0 and self.bomb):
               self._bomb(self.facing, self._get_tile())
            
               self.bombcooldown = Player.BOMB_COOLDOWN
               pass#TODO BOMB SOUNDS          
               
          elif(self._pressed("BOMB")):
               pass#TODO fail sounds
               
          self.bombcooldown -= elapsed
          
      
     def avoid_police(self, police):
        ''' ('Player', 'Police') -> None
        The player will not be able to move for 3 seconds after he/she has 
        been caught by a guard.
        '''    	
        #TODO: fix so it actually works
        if (self.stasis==0 and police.get_rect().colliderect(self.get_rect())):
            self.velocity.y = 0
            self.velocity.x = 0
            
            police.wander()
        
     def render(self,canvas):
          canvas.blit(Player.placeholders[self.facing],
                      (self.x - self.parent.camerax,
                       self.y - self.parent.cameray -
                           Player.placeholders[self.facing].get_size()[1])
                      )
      
     def _pressed(self,code):
          return pygame.key.get_pressed()[self.keybindings[code]]
     
     def _bomb(self, direction, tile):
          tile.paint_color = self.color
          tile.player_number = self.player_number
          if not(tile.get_neighbor(self.facing).raised):
             self._bomb(direction, tile.get_neighbor(self.facing))
             self.explosion.play()
          
               

class Police(LivingEntity):
     
     SPEED_DEFAULT=200
     SPEED_FAST=200
     FAST_TIME=1.5
     CHASE_TIME=5
     
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
          
          self.size = Point(40,40)
          self.rect_offset = Point(5,5)
          
          self.speed = Police.SPEED_DEFAULT
          self.fasttimer=0
          
          self.target = None
          self.time_chasing = 0
     
     def update(self, elapsed):
          self.velocity.y=0
          self.velocity.x=0
          self.time_chasing-=elapsed
          
          if(self.destination is None):
               
               if(self.target == None):
                    if(random.random()<0.2*elapsed):
                         self.facing= (self.facing-1)%3
                    if(random.random()<(0.2-0.15*(self._get_tile().paint_color is not None))*elapsed):
                         self.wander()
                    
               elif self.time_chasing<=0:
                    self.target=None
               elif self.target._get_tile()==this.get_tile():
                    if(self.x!=self.target.x):
                         self.velocity.x=self.speed * get_sign(self.target.x-self.x)
                         self.facing = 1+2*(self.velocity.x<0)
                         if(math.abs(self.x-target.x<self.speed)):
                            self.velocity.x=0
                            self.x=target.x
                    if(self.y!=(self.path[0].gridy+0.5)*maingame.GRID_RESOLUTION):
                         self.velocity.y=self.speed * get_sign(self.target.y-self.y)
                         self.facing = 0+2*(self.velocity.y<0)
                         if(math.abs(self.y-target.y<self.speed)):
                              self.velocity.y=0
                              self.y=target.y                         
               else:
                    self.destination = self.target._get_tile()
                    self.path = self.find_path(self._get_tile(),self.destination)[1:]                    
          else:
               if(self.speed==Police.SPEED_FAST and time.time()-self.fasttimer>Police.FAST_TIME):
                    self.speed = Police.SPEED_DEFAULT
               
               if(self.destination == self._get_tile() or
                  (len(self.path)==1 and elapsed*random.random()<=0.2 and not self.speed==Police.SPEED_FAST) ):#reduce chance of stacking
                    self.look_at(self.destination)
                    self.destination = None
               else:
                    #print abs(self.x - self.path[0].gridx*maingame.GRID_RESOLUTION), abs(self.y - self.path[0].gridy*maingame.GRID_RESOLUTION), Police.SPEED
                    #if close enough ,switch to next node
                    if(abs(self.x - self.path[0].gridx*maingame.GRID_RESOLUTION)<self.speed*elapsed and
                       abs(self.y - (self.path[0].gridy+0.5)*maingame.GRID_RESOLUTION)<self.speed*elapsed):
                         self.x = self.path[0].gridx*maingame.GRID_RESOLUTION
                         self.y = (self.path[0].gridy+0.5)*maingame.GRID_RESOLUTION
                         self.path = self.path[1:]
                    #otherwise, move to next node on path.
                    else:
                         if(self.x!=self.path[0].gridx*maingame.GRID_RESOLUTION):
                              self.velocity.x=self.speed * get_sign(self.path[0].gridx*maingame.GRID_RESOLUTION-self.x)
                              self.facing = 1+2*(self.velocity.x<0)
                         if(self.y!=(self.path[0].gridy+0.5)*maingame.GRID_RESOLUTION):
                              self.velocity.y=self.speed * get_sign((self.path[0].gridy+0.5)*maingame.GRID_RESOLUTION-self.y)
                              self.facing = 0+2*(self.velocity.y<0)
                              
          super(Police,self).update(elapsed)
                            
     
     def wander(self):
          '''
          A police officer which has come into contact with a player will find a new destination.
          '''
          while(self.destination is None or self.destination.raised):

               self.destination = random.choice(random.choice(self.parent.map_tiles))
          self.path = self.find_path(self._get_tile(),self.destination)[1:]

     def render(self,canvas):
          canvas.blit(Police.policeimages[self.facing],
                      (self.x - self.parent.camerax,
                       self.y - self.parent.cameray -
                           Police.policeimages[self.facing].get_size()[1])
                      )
     
     def get_vision_rect(self):
          return[
               pygame.rect.Rect(self.x,self.y,50,200),
               pygame.rect.Rect(self.x,self.y,200,50),
               pygame.rect.Rect(self.x,self.y-150,50,200),
               pygame.rect.Rect(self.x-150,self.y,200,50),
          ][self.facing]
     
     def alert_to(self, player, maptile,isfast=False):
         ''' 
         If a guard notices a player through one of the security cameras, he will 
         approach the player. At the time that the guard reaches the player, he will stop
         moving closer.
         '''
         if(self.destination is None and not self.get_rect().colliderect(player.get_rect())):
               if(isfast and self.speed!=Police.SPEED_FAST):
                              self.fasttimer = time.time()
                              self.speed = Police.SPEED_FAST               
               self.destination = player._get_tile()
               self.path = self.find_path(self._get_tile(),self.destination)[1:]
               #print self.path
               self.parent.add(Exclamation(self.x+20, self.y))
          
     def find_path(self, current_tile, destination, path=[], cumscore=0):
          if current_tile == destination:
               return path+[current_tile]
          workingtiles=current_tile.get_surrounding(True)
          
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
     
     def __init__(self,x,y, initialtime = 0, rotation_modifer = 0):
          super(Camera, self).__init__(x,y)
          self.last_rotation = time.time()+ initialtime
          self.rotation_mod = rotation_modifer
          self.facing = random.randint(0,3)
          
          self.monitor_rects = [
               pygame.rect.Rect(self.x-1,self.y+maingame.GRID_RESOLUTION,maingame.GRID_RESOLUTION, maingame.GRID_RESOLUTION*2),
               pygame.rect.Rect(self.x+-1+maingame.GRID_RESOLUTION,self.y,maingame.GRID_RESOLUTION*2,maingame.GRID_RESOLUTION),
               pygame.rect.Rect(self.x-1,self.y-maingame.GRID_RESOLUTION,maingame.GRID_RESOLUTION,maingame.GRID_RESOLUTION*2),
               pygame.rect.Rect(self.x-1+maingame.GRID_RESOLUTION*2,self.y,maingame.GRID_RESOLUTION*2,maingame.GRID_RESOLUTION)
               ]
     
     def update(self,elapsed):
          if(time.time() - self.last_rotation > Camera.rotation_time + self.rotation_mod):
               self.facing  = (self.facing+1)%4
               self.last_rotation = time.time()
               
     
     def render(self,canvas):
          canvas.blit(Camera.cameraimages[self.facing],
                                (self.x - self.parent.camerax,
                                 self.y - self.parent.cameray -
                                 Camera.cameraimages[self.facing].get_size()[1]))
          
     
     def post_render(self,canvas):
          pygame.draw.rect(canvas,
                           pygame.color.Color(255,0,0,50),
                           self.get_vision_rect().copy()
                           .move(- self.parent.camerax, - self.parent.cameray),
                           1)
     
     def get_vision_rect(self):
          return self.monitor_rects[self.facing]

class Exclamation(Entity):
     
     mark = pygame.image.load(os.getcwd()+"/res/exclaim.png")     
     blip = None

     def __init__(self,x,y):
          super(Exclamation,self).__init__(x,y)
          self.velocity.y=-50
          self.friction=5
          self.age=0
          if(Exclamation.blip is None):
               Exclamation.blip = pygame.mixer.Sound(os.getcwd()+"/res/blip_noticed.wav")
          Exclamation.blip.play()
     
     def update(self,elapsed):
          super(Exclamation,self).update(elapsed)
          self.velocity.y-=self.velocity.y*10*elapsed
          self.age+=elapsed
          if(self.age>=1):
             self.alive=False
          
     
     def render(self,canvas):
          Exclamation.mark.set_alpha( 255*(1 - self.age/1) )     
          canvas.blit(Exclamation.mark,(self.x,self.y))
