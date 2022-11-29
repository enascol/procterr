from ursina import *
from numpy import floor

import random
import settings

ALPHA = settings.BLOCK_ALPHA

base_colors = {
    "cloud": (255, 255, 255, ALPHA),
    "ice": (58, 146, 194, ALPHA),
    "rock": (50, 52, 54, ALPHA),
    "lava": (194, 74, 58, ALPHA),
    "grass": (66, 110, 48, ALPHA),
    "dirt": (59, 39, 36, ALPHA)
}

MOD_25 = [random.randint(1, 10) / 10 for _ in range(3)]
MOD_50 = [random.randint(1, 10) / 10 for _ in range(3)]
MOD_75 = [random.randint(1, 10) / 10 for _ in range(3)]
MOD_100 = [random.randint(1, 10) / 10 for _ in range(3)]

X_TERRAIN_25 = floor(settings.TERRAIN_WIDTH * 0.25)
X_TERRAIN_50 = floor(settings.TERRAIN_WIDTH * 0.50)
X_TERRAIN_75 = floor(settings.TERRAIN_WIDTH * 0.75)

def get_color_modifier(region):
    return settings.REGIONS_COLOR[region]

def modify_color(color, region, mod=True):
    if not mod:
        r, g, b, alpha = base_colors[color]
    else:
        r, g, b, alpha = get_color_modifier(region)[color]

    return r, g, b, alpha

def get_terrain_elevation(z):
    if z <= X_TERRAIN_25:
        return 1, 1
    elif z > X_TERRAIN_25 and z <= X_TERRAIN_50:
        return 35, 70
    elif z > X_TERRAIN_50 and z <= X_TERRAIN_75:
        return 1, 4
    elif z > X_TERRAIN_75:
        return 10, 30

def place_weird_veg(cube):
    x, y, z = cube.position
    
    if y == 0:
        if random.randint(1, 100) < settings.WEIRD_VEG_PROBABILITY:
            Entity(
                model = "weird_veg",
                texture = "basic",
                collider = None,
                color = cube.color,
                scale = random.randint(1, 10) / 10,
                position = (x, 0.5, z)
            )

def place_clouds(cube):
    x, y, z = cube.position

    if y > 10:
        Entity(
            model = "cube",
            color = color.white,
            collider = None,
            position = (x, y + 20, z)
        )


