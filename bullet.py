import pygame
from bombsupport import import_folder
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        #
        self.animations = {}
        self.import_character_assets()
        self.animation_speed = 0.05
        self.frame_index = 0
        self.image = pygame.image.load("bomb (1).png")
        self.image = pygame.transform.scale(self.image, (40,63.3))
        self.rect = self.image.get_rect(center=pos)
        self.bomb_timer = pygame.time.get_ticks() + 2000
        self.transparent_timer = pygame.time.get_ticks() + 500
        self.pos = pos
        self.exploding = False
        self.visible = True
        self.transparent = True
        self.animation = []
        self.hitbox = 0
        self.sound_played = False
        self.spawn_effect = pygame.mixer.Sound("jump.mp3")
        pygame.mixer.Sound.play(self.spawn_effect)
        self.bomb_effect = pygame.mixer.Sound("explodesound.mp3")



    def import_character_assets(self):
        character_path = "avatar/"
        self.animations = {"explodeanimation":[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        self.animation = self.animations["explodeanimation"]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation)-1:
            self.visible = False
            self.kill()
        self.image = self.animation[int(self.frame_index)]


    def update(self):
        if self.visible:
            if self.exploding:
                self.image = self.animations["explodeanimation"][int(self.frame_index)]
                self.animate()
            if pygame.time.get_ticks() >= self.transparent_timer:
                self.transparent = False

