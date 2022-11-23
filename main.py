from ursina import *
import time
import sounds

from level import Level
from player import Player
from sun import Sun
from numpy import abs
from settings import TERRAIN_WIDTH, FOG_COLOR, FOG_DENSITY
from builder import BuilderTool

app = Ursina()

player = Player()
previous_z = player.z
previous_x = player.x
previous_time = time.time()

sky = Sky(texture="textures/dead_stars_night_sky")

R, G, B = FOG_COLOR
scene.fog_density = FOG_DENSITY
scene.fog_color = color.rgb(R, G, B)
window.fullscreen = True
b = BuilderTool()
level = Level(player)
player.x = floor(TERRAIN_WIDTH/2)
player.z = floor(TERRAIN_WIDTH/2)
player.y = 100
level.generate_chunk()

def input(key):
    if key == "left mouse up":
        b.place()

class Color:
    r = 0
    g = 0
    b = 0

def update():
    global previous_time
    if abs(player.z - previous_z) > 1 or abs(player.x - previous_x) > 1:
        level.generate_chunk()
    
    if time.time() - previous_time > 0.1:
        level.generate_subset()

app.run()

