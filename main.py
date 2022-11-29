from ursina import *
import time
import settings

from level import Level
from player import Player
from sun import Sun
from numpy import abs
from builder import BuilderTool

app = Ursina()

player = Player()
previous_z = player.z
previous_x = player.x
previous_time = time.time()

#sky = Sky(texture="textures/dead_stars_night_sky")

R, G, B = settings.FOG_COLOR
scene.fog_density = settings.FOG_DENSITY
scene.fog_color = color.rgb(R, G, B)
window.fullscreen = True
b = BuilderTool()
level = Level(player)
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
    
    level.generate_subset()
    level.update_rock()

top_view = False

def input(key):
    if key == "page up":
        global top_view

        if not top_view:
            scene.fog_density = 0
            
            player.y = floor(settings.AMP * 1.25)
            player.x = floor(settings.TERRAIN_WIDTH/2)
            player.z = floor(settings.TERRAIN_WIDTH/2)
            player.gravity = 0
            
            top_view = True
        else:
            scene.fog_density = settings.FOG_DENSITY
            
            player.x = floor(settings.TERRAIN_WIDTH/2)
            player.z = floor(settings.TERRAIN_WIDTH/2)
            player.gravity = 1

            top_view = False
        
    if key == "scroll down" and top_view:
        player.y += 1
    elif key == "scroll up" and top_view:
        player.y += -1

app.run()

