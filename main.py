from ursina import *
import time
import sounds

from level import Level
from player import Player
from sun import Sun
from numpy import abs
from settings import TERRAIN_WIDTH

app = Ursina()

player = Player()

previous_z = player.z
previous_x = player.x

previous_time = time.time()

sky = Sky(texture="textures/dead_stars_night_sky")

#window.fullscreen = True

#scene.fog_density = 0.9
#scene.fog_color = color.rgb(0, 0, 0)

level = Level(player)
level.generate_chunk()

def update():
    global previous_time
    if abs(player.z - previous_z) > 1 or abs(player.x - previous_x) > 1:
        level.generate_chunk()
    
    if time.time() - previous_time > 0.1:
        level.generate_subset()
        #previous_time = time.time()

app.run()

