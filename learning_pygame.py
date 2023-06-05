import pygame as py, sys
from settings import * # * means bring all values from file
from level import Level
py.mixer.init()
py.init() # Initialise Pygame
screen = py.display.set_mode((screen_width,screen_height)) # Screen dimensions, width/height
clock = py.time.Clock() # Ensures consistent performance across devices
level = Level(level_map, screen)
while True:
    # Will quit pygame when user clicks button to close window
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit() # Will quit pygame
            sys.exit() # 'sys' used to exit program
    bg = py.image.load('grassbackground.png')
    bg = py.transform.scale(bg, (screen_width, screen_height))
    screen.blit(bg, (0, 0))
    level.run()
    py.display.update() # Will refresh screen for user

    clock.tick(fps) # Number of times the loop will run_right per second



