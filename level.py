import pygame, random
from settings import tile_size, screen_height, screen_width, exploding_bombs, active_bombs
from tile import Tile
from player import Player
from bullet import Bullet
from speed_powerup import speed_powerup
from capacity_powerup import capacity_powerup
import time
from guizero import info
from random import randint


class Level:
    def __init__(self, level_data, surface):

        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.speed_powerups = pygame.sprite.Group()
        self.capacity_powerups = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.destructables = pygame.sprite.Group()
        self.setup_level(level_data)
        self.exploding_bombs = []
        pygame.mixer.music.load("backgroundm.mp3")
        self.powerup_sound = pygame.mixer.Sound("powersound.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.25)
        # https://chat.openai.com/share/43a17db3-e67d-4809-a4fe-21b1cf24c335
        self.speed_powerup_timer = pygame.time.set_timer(pygame.USEREVENT + 1, 4000)
        self.capacity_powerup_timer = pygame.time.set_timer(pygame.USEREVENT + 2, 4000)
    def spawn_enemies(self):
        for i in range(3):
            enemy = speed_powerup((random.randint(300, screen_width), random.randint(0, screen_height)))
            self.speed_powerups.add(enemy)
    def spawn_enemies_2(self):
        enemy1 = capacity_powerup((random.randint(300, screen_width), random.randint(0, screen_height)))
        self.capacity_powerups.add(enemy1)

    def setup_level(self,layout):
        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                x = cell_index*tile_size
                y = row_index*tile_size
                if cell == "x":
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)
                elif cell == "p":
                    player_sprite1 = Player((x,y),True)
                    self.player.add(player_sprite1)
                elif cell == "o":
                    player_sprite2 = Player((x,y),False)
                    self.player.add(player_sprite2)


    def run(self):
        self.player.update(self.tiles)
        self.tiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.speed_powerups.draw(self.display_surface)
        self.capacity_powerups.draw(self.display_surface)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self.spawn_enemies()
            if event.type == pygame.USEREVENT + 2:
                self.spawn_enemies_2()

        for player in self.player:
            if player.health == 0:
                pygame.quit()
            player.draw_bullets(self.display_surface)
            collided_with = pygame.sprite.spritecollide(player, self.speed_powerups, True)
            if collided_with:
                pygame.mixer.Sound.play(self.powerup_sound)
                player.speed_powered_up = True
                player.speed_powerup(time.time())
            collided_with_2 = pygame.sprite.spritecollide(player, self.capacity_powerups, True)
            if collided_with_2:
                pygame.mixer.Sound.play(self.powerup_sound)
                player.capacity_powered_up = True
                player.capacity_powerup(time.time())
        for bullet in active_bombs:
            if pygame.time.get_ticks() >= bullet.bomb_timer:
                bullet.exploding = True
                if not bullet.sound_played:
                    pygame.mixer.Sound.play(bullet.bomb_effect)
                    bullet.sound_played = True
                exploding_bombs.append(bullet)
        for b in exploding_bombs:
            if b.visible and b.exploding:
                hitbox_sprite = pygame.sprite.Sprite()
                b.hitbox = pygame.draw.circle(self.display_surface, (255, 0, 0), (b.rect.centerx, b.rect.centery), 100)
                hitbox_sprite.rect = b.hitbox
                kill_players = pygame.sprite.spritecollide(hitbox_sprite, self.player, True)
                for p in kill_players:
                    p.eliminate()
            else:
                b.kill()

