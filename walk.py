from ursina import *
from player import Player
from numpy import floor

app = Ursina()

level = open("D:\Python\drunken_walk\matrixes\level").readlines()

level = [line.strip() for line in level]

rows = len(level)
columns = len(level[0])
level_parent = Entity(collider = "mesh")

scene.fog_color = color.rgb(0, 0, 0)
scene.fog_density = 0.2

Sky(texture="dark")

player = Player()

while True:
    x, z = random.randint(0, columns-1), random.randint(0, rows-1)
    if level[x][z] != "#":
        player.x = x
        player.z = z
        player.y = 5
        break

def get_n(x, z):
    directions = [
        (x + 1, z),
        (x - 1, z),
        (x, z + 1),
        (x, z - 1)
    ]
    
    directions = [pos for pos in directions if 0 <= pos[0] < columns and 0 <= pos[1] < rows]
    return [level[pos[0]][pos[1]] == "#" for pos in directions]

colors = {}

for x in range(rows):
    for z in range(columns):
        value = level[x][z]

        if value == "#" and all(get_n(x, z)):
            continue
        if value == "#":
            Button(
                parent = level_parent, 
                collider = "box", 
                model ="cube",
                position = (x, 0, z), 
                scale = (1, 5, 1),
                color = color.rgb(255, 0, 0, 50)
                )
        else:
            try:
                c = colors[value]
            except KeyError:
                r, g, b = [random.randint(0, 255) for x in range(3)]
                c = color.rgb(r, g, b)
                colors[value] = c

            Button(
                parent = level_parent, 
                collider = None, 
                model = "cube", 
                position = (x, 0, z), 
                color = c,
                highlight = color.black
            )

player.disable()
level_parent.combine(auto_destroy=False)
player.enable()


top_view = False

terrain_size = 6
cubes = []

for i in range(terrain_size ** 2):
    cube = Entity(
        model = "cube",
        collider = "box",
        color = color.green
    )

    cubes.append(cube)

#x = self.chunks[i].x = floor((i / self.chunk_width) + player_pos_x - 0.5 * self.chunk_width)
#z = self.chunks[i].z = floor((i % self.chunk_width) + player_pos_z - 0.5 * self.chunk_width)

def generate_terrain():
    for i in range(terrain_size ** 2):
        x = cubes[i].x = floor((i / terrain_size) + player.x - 0.5 * terrain_size)
        z = cubes[i].z = floor((i % terrain_size) + player.z - 0.5 * terrain_size)
        y = cubes[i].y = 0
        cubes[i].visible = False

def input(key):

    if key == "page up":
        global top_view
        if top_view:
            player.gravity = 1
            top_view = False
            scene.fog_density = 0.2
        else:
            player.gravity = 0
            player.y = 35
            player.x = int(len(level) / 2)
            player.z = int(len(level[0]) / 2)
            top_view = True
            scene.fog_density = 0
    
    if top_view:
        if key == "scroll  down":
            player.y += 1
        elif key == "scroll up":
            player.y -= 1

generate_terrain()

def update():
    generate_terrain()

app.run()