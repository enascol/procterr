from ursina import *
from player import Player

import random

app = Ursina()
player = Player(position = (0, 0, 0))
current_x = player.x
current_z = player.z
player.gravity = 0

#Sky(texture ="dark")
scene.fog_density = 0.04
scene.fog_color = color.rgb(0, 0, 0)
maze = Entity(
    model = "drunken1"
)
app.run()