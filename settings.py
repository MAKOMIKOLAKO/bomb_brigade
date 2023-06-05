"""
Used for any kinds of variables that have to be accessed across the entire project
"""
from guizero import App

"""level_map = [
            "                 ",
            "                 ",
            "  x  x  x  x  x  ",
            "                 ",
            "        o        ",
            "  x  x  x  x  x  ",
            "                 ",
            "     p           ",
            "                 "]"""
"""level_map = [
    "                      ",
    "                      ",
    "  x  x  x  x  x  x  x ",
    "                      ",
    "         o            ",
    "  x  x  pooox  x  x  x  x ",
    "                      ",
    "     p                ",
    "  x  x  x  x  x  x  x ",
    "                      ",
    "                      ",
    "  x  x  x  x  x  x  x ",
    "                      ",
    "                      ",
    "                      "
]"""
level_map = [
    "                 ",
    "                 ",
    "  x  x  x  x  x  ",
    "                 ",
    "         o       ",
    "  x  x  x  x  x  ",
    "                 ",
    "     p           ",
    "  x  x  x  x  x  ",
    "                 ",
    "                 ",

]

tile_size = 60
#screen_width = 1100
screen_height = len(level_map) * 60
active_bombs = []
exploding_bombs = []
screen_width = 1150
fps = 60



