import pygame
from bullet import Bullet
from support import import_folder
from settings import screen_width, screen_height, exploding_bombs, active_bombs
import time
class Player(pygame.sprite.Sprite):

    def __init__(self, pos, controls):
        super().__init__()
        self.animations = {}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.controls = controls
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4
        self.bullets = pygame.sprite.Group()
        self.firing = False
        self.status="idle"
        self.health = 100
        self.speed_powered_up = False
        self.capacity_powered_up = False
        self.drop_gap = 1000
        self.drop_timer = pygame.time.get_ticks() + self.drop_gap


    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def speed_powerup(self, settime):
        global time_set
        time_set = settime
        if self.speed_powered_up:
            self.speed=8
        else:
            self.speed = 4

        if time.time() - settime > 5:
            self.speed_powered_up = False
            self.speed = 4

    def capacity_powerup(self, settime):
        global time_set_1
        time_set_1 = settime
        print('capacity increased')
        if self.capacity_powered_up:
            self.drop_gap=250
        else:
            self.drop_gap=1000

        if time.time() - settime > 3:
            self.capacity_powered_up = False
            self.drop_gap = 1000



    def import_character_assets(self):
        character_path = "avatar/"
        self.animations = {"idle":[], "run_right":[], "run_left":[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    def eliminate(self):
        self.health = 0
        print('game is over!!!')

    def get_status(self):
        if self.direction.x == 0 and self.direction.y==0:
            self.status = 'idle'
        elif self.direction.x > 0:
            self.status = 'run_right'
        elif self.direction.x < 0:
            self.status = 'run_left'
        elif self.direction.y != 0 and self.direction.x==0:
            self.status = 'run_right'

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        if self.controls:
            if keys[pygame.K_d] and self.rect.right<screen_width:
                self.direction.x = 1
            elif keys[pygame.K_a] and self.rect.left>0:
                self.direction.x = -1
            elif keys[pygame.K_w] and self.rect.top > 0:
                self.direction.y = -1
            elif keys[pygame.K_s] and self.rect.bottom < screen_height:
                self.direction.y = 1
            if pygame.time.get_ticks()>self.drop_timer:
                self.firing = False
            else:
                self.firing = True
            if keys[pygame.K_SPACE] and not self.firing:
                self.fire()
                self.firing = True
                self.drop_timer = pygame.time.get_ticks() + self.drop_gap

            elif not keys[pygame.K_SPACE] and self.firing:
                self.firing = False
        else:
            if keys[pygame.K_RIGHT] and self.rect.right<screen_width:
                self.direction.x = 1
            elif keys[pygame.K_LEFT] and self.rect.left>0:
                self.direction.x = -1
            elif keys[pygame.K_UP] and self.rect.top > 0:
                self.direction.y = -1
            elif keys[pygame.K_DOWN] and self.rect.bottom < screen_height:
                self.direction.y = 1
            else:
                self.direction.x = 0
                self.direction.y = 0
            if pygame.time.get_ticks()>self.drop_timer:
                self.firing = False
            else:
                self.firing = True
            if keys[pygame.K_p] and not self.firing:
                self.fire()
                self.firing = True
                self.drop_timer = pygame.time.get_ticks() + self.drop_gap

            elif not keys[pygame.K_p] and self.firing:
                self.firing = False

    def horizontal_movement_collision(self, tiles):
        # Function to handle horizontal collisions
        self.rect.x += self.direction.x * self.speed

        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = tile.rect.right
                elif self.direction.x > 0:
                    self.rect.right = tile.rect.left

        for b in active_bombs:
            if b.visible and not b.transparent:
                if not b.transparent:
                    if b.rect.colliderect(self.rect):
                        if self.direction.x < 0:
                            self.rect.left = b.rect.right
                        elif self.direction.x > 0:
                            self.rect.right = b.rect.left

    def vertical_movement_collision(self, tiles):
        # Function to handle vertical collisions
        self.rect.y += self.direction.y * self.speed # Changes vertical position of avatar, increased by speed (set in settings)
        for tile in tiles.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                elif self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
        for b in active_bombs:
            if b.visible and not b.transparent:
                if b.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = b.rect.top
                    elif self.direction.y < 0:
                        self.rect.top = b.rect.bottom

    def fire(self):
        bullet = Bullet((self.rect.centerx, self.rect.centery))
        self.bullets.add(bullet)
        active_bombs.append(bullet)

    def draw_bullets(self, surface):
        self.bullets.draw(surface)

    def update(self, tiles):
        self.get_input()
        self.horizontal_movement_collision(tiles)
        self.vertical_movement_collision(tiles)
        self.bullets.update()
        self.get_status()
        self.animate()
        if self.speed_powered_up:
            self.speed = 8
            if abs(time.time() - time_set) > 5:
                self.speed_powered_up = False
                self.speed = 4
        if self.capacity_powered_up:
            self.drop_gap = 250
            if abs(time.time()-time_set_1) > 3:
                self.capacity_powered_up = False
                self.drop_gap = 1000
