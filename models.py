import arcade
import random
import math


SCALE = 0.5
OFFSCREEN_TOWN = 300
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LEFT_LIMIT = -OFFSCREEN_TOWN
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_TOWN
BOTTOM_LIMIT = -OFFSCREEN_TOWN
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_TOWN


class TurningSprite(arcade.Sprite):

    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))

class ActorSprite(arcade.Sprite):

    def __init__(self, filename, scale):
      
        super().__init__(filename, scale)
        
        self.respawning = 0
        self.respawn()

    def respawn(self):
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0

    def update(self):
        super().update()
        if self.respawning:
            self.respawning += 1
            self.alpha = self.respawning / 500.0
            if self.respawning > 250:
                self.respawning = 0
                self.alpha = 1
                
        if self.center_x < 0:
            self.center_x = SCREEN_WIDTH
        if self.center_x > SCREEN_WIDTH:
            self.center_x = 0
        if self.center_y > SCREEN_HEIGHT:
            self.center_y = 0
        if self.center_y < 0:
            self.center_y = SCREEN_HEIGHT      
        
class zombieSprite(arcade.Sprite):

    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0
    
    def zombie_angle(x1,y1,x2,y2):
        return -math.degrees(math.atan2(x1-x2 , y1-y2))
    
    def follow_player(self, player):
        if random.randrange(1000000)>900000:
            self.angle = zombieSprite.zombie_angle(self.center_x,
                                                   self.center_y, 
                                                   player.center_x,
                                                   player.center_y)
        else:
            self.angle += 0.005 
    
    def update(self):
  
        self.change_x = math.cos(self.angle)*3/5
        self.change_y = math.sin(self.angle)*3/5
        

        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT
    
        super().update()


class BulletSprite(TurningSprite):

    def update(self):
        super().update()
        if self.center_x < -100 or self.center_x > 1500 or \
                self.center_y > 1100 or self.center_y < -100:
            self.kill()
