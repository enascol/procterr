from ursina import *
import time
import sounds

from level import Level
from player import Player
from sun import Sun
from numpy import abs
from settings import TERRAIN_WIDTH
from builder import BuilderTool

app = Ursina()

player = Player()

previous_z = player.z
previous_x = player.x

previous_time = time.time()

sky = Sky(texture="textures/dead_stars_night_sky")

window.fullscreen = False

scene.fog_density = 0.04
scene.fog_color = color.rgb(0, 0, 0)

b = BuilderTool()
level = Level(player)
level.generate_chunk()

def input(key):
    if key == "left mouse up":
        b.place()

def update():
    global previous_time
    if abs(player.z - previous_z) > 1 or abs(player.x - previous_x) > 1:
        level.generate_chunk()
    
    if time.time() - previous_time > 0.1:
        level.generate_subset()
    
    
    #b.select(player)


app.run()

