import random
import math
import arcade
import models

SCALE = 1
OFFSCREEN_TOWN = 300
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LEFT_LIMIT = -OFFSCREEN_TOWN
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_TOWN
BOTTOM_LIMIT = -OFFSCREEN_TOWN
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_TOWN


class MyWindow(arcade.Window):


    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.frame_count = 0
        
        self.game_over = False
        
        self.all_sprites_list = None
        self.zombie_list = None
        self.bullet_list = None
        self.actor_life_list = None

        self.score = 0
        self.player_sprite = None
        self.lives = 3
        
        arcade.set_background_color(arcade.color.BLACK)
        
        self.bullet_sound = arcade.load_sound("sounds/laser1.mp3")
        self.zombie_sound = arcade.load_sound("sounds/zombie.mp3")

        self.score_text = None
        self.zombie_text = None

    def start_new_game(self):

        self.frame_count = 0
        self.game_over = False

        self.all_sprites_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.actor_life_list = arcade.SpriteList()

        self.score = 0
        self.player_sprite = models.ActorSprite("images/actor.png", SCALE)
        self.all_sprites_list.append(self.player_sprite)
        self.lives = 3

        cur_pos = 10
        
        for i in range(self.lives):
            life = arcade.Sprite("images/heart.png", SCALE/5)
            life.center_x = cur_pos + life.width
            life.center_y = life.height
            cur_pos += life.width
            self.all_sprites_list.append(life)
            self.actor_life_list.append(life)
        
        self.make_zombie(1)

    def on_draw(self):

        arcade.start_render()

        self.all_sprites_list.draw()

        output = f"Score: {self.score}"
        
        if not self.score_text or output != self.score_text.text:
            self.score_text = arcade.create_text(output, arcade.color.WHITE, 14)
        arcade.render_text(self.score_text, 10, 70)

        output = "Level: {}".format(self.score//30)
        if not self.zombie_text or output != self.zombie_text.text:
            self.zombie_text = arcade.create_text(output, arcade.color.WHITE, 14)
        arcade.render_text(self.zombie_text, 10, 50)

    def on_key_press(self, symbol, modifiers):
       
        if not self.player_sprite.respawning and symbol == arcade.key.SPACE:
            bullet_sprite = models.BulletSprite("images/bullet.png", SCALE)

            bullet_speed = 13
            
            
            
            bullet_sprite.change_y = math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
            bullet_sprite.change_x = -math.sin(math.radians(self.player_sprite.angle)) * bullet_speed
            

            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y

            bullet_sprite.update()

            self.all_sprites_list.append(bullet_sprite)
            self.bullet_list.append(bullet_sprite)

            arcade.play_sound(self.bullet_sound)

        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        
            


    def on_key_release(self, symbol, modifiers):
   
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0

    def make_zombie(self , n):
        for i in range(n):
                image_no = random.randrange(4)
                image_list = ("images/zombie1.png",
                      "images/zombie2.png",
                      "images/zombie3.png",
                      "images/zombie4.png")

                enemy_sprite = models.zombieSprite(image_list[image_no],
                                              SCALE *1)

                enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT ,TOP_LIMIT )
                print(enemy_sprite.center_y )
                if enemy_sprite.center_y>0:
                    if random.randrange(2)==0:
                        enemy_sprite.center_x = 1000/2 + math.sqrt(780*780-(enemy_sprite.center_y-600)*(enemy_sprite.center_y-600))
                    else:
                        enemy_sprite.center_x = 1000/2 - math.sqrt(780*780-(enemy_sprite.center_y-600)*(enemy_sprite.center_y-600))
                else:
                    if random.randrange(2)==0:
                        enemy_sprite.center_x = 1000/2 + math.sqrt(780*780-(enemy_sprite.center_y+600)*(enemy_sprite.center_y+600))
                    else:
                        enemy_sprite.center_x = 1000/2 - math.sqrt(780*780-(enemy_sprite.center_y+600)*(enemy_sprite.center_y-600))
                    
         
                
               # enemy_sprite.size = 4

                self.all_sprites_list.append(enemy_sprite)
                self.zombie_list.append(enemy_sprite)
                
                
                
    def add_zombie_and_score(self, asteroid: models.zombieSprite):

        x = asteroid.center_x
        y = asteroid.center_y
        self.score += 1
        
        while len(self.zombie_list)<20:
            self.make_zombie(2+2*self.score//10)
            
        
    def update(self, x):

        self.frame_count += 1

        if not self.game_over:
            self.all_sprites_list.update()

            for bullet in self.bullet_list:
                zombies = \
                    arcade.check_for_collision_with_list(bullet, self.zombie_list)
                for zombie in zombies:
                    self.add_zombie_and_score(zombie)
                    zombie.kill()
                    arcade.play_sound(self.zombie_sound)
                    bullet.kill()

            if not self.player_sprite.respawning:
                zombies = \
                    arcade.check_for_collision_with_list(self.player_sprite,
                                                         self.zombie_list)
                if len(zombies) > 0:
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        self.add_zombie_and_score(zombies[0])
                        zombies[0].kill()
                        self.actor_life_list.pop().kill()
                        
                        print("Crash")
                        
                        for zombie in self.zombie_list:
                            zombie.kill()
                        for zombie in self.zombie_list:
                            zombie.kill()
                        for zombie in self.zombie_list:
                            zombie.kill()
                        for zombie in self.zombie_list:
                            zombie.kill()
                        for zombie in self.zombie_list:
                            zombie.kill()
                        self.make_zombie(2)
                                                
                        
                    else:
                        for zombie in self.zombie_list:
                            zombie.kill()
                            
                        self.game_over = True
                        print("Game over")


def main():
    window = MyWindow()
    window.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()

