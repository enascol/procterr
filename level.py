from block import Block
from numpy import floor
from perlin_noise import PerlinNoise
from ursina import *
from voxel import Voxel
<<<<<<< HEAD
from perlin_noise import PerlinNoise
from numpy import floor
from ursina.shaders import lit_with_shadows_shader
=======


import parse_terrain
import settings
>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a

import settings

class Level:

    def __init__(self, player):
        self.player = player 

        # Terrain info
        self.terrain_width = settings.TERRAIN_WIDTH
<<<<<<< HEAD
        self.terrain = Entity(model = None, collider =None)
        self.terrain_finished = False

        # Procedural generation params
        self.noise = PerlinNoise(octaves = settings.OCTAVE, seed = random.randint(1, 50000))
        self.freq = settings.FREQUENCY
        self.amp = settings.AMP
=======
        self.terrain = Block(model = None, collider =None)
        self.terrain_finished = False

        # Procedural generation params
        self.noise = PerlinNoise(octaves = settings.OCTAVE, seed = settings.SEED)
        self.freq = settings.FREQUENCY
        self.amp = settings.AMP
        print(f"\n[*] Generating terrain with seed #{settings.SEED}\n")
>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a

        # Terrain chunk settings
        # This terrain is small enough to be walked on
        # and will be only rendered as you walk.
        # Its also invisible
        self.chunk_width = 6
        self.chunks = [Block(model = "cube", collider = "box") for _ in range(self.chunk_width ** 2)]

        # Subsets settings
        # This is the visible terrain
        # Its faster to load since wont have a collision mesh
        self.sub_width = self.terrain_width
        self.subcube_index = 0
        self.current_subset = 0
        self.subcubes = [Block(model = "cube", player = self.player) for _ in range(self.sub_width)]
        self.subsets = [Block(model = None) for _ in range(int((self.terrain_width ** 2) / self.sub_width))]

<<<<<<< HEAD
        self.sky = Entity(collider =None, texture =None, model =None)
        self.movement_direction = 1
        self.stars = []

        self.place_smiling_orb()
=======
        self.sky = Block(collider =None, texture =None, model =None)
        self.movement_direction = 1
        self.stars = []

        self.veg_parent = Block(model = None)

        self.falling_rock()
>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a

    def set_basic_terrain(self):
        for i in range(self.terrain_width ** 2):
            cube = Entity(model = 'models/grass')
            cube.x = floor(i / self.terrain_width)
            cube.z = floor(i % self.terrain_width)
            cube.y = floor((self.noise([cube.x / self.freq, cube.z / self.freq])) * self.amp)
            cube.parent = self.terrain
        
        self.terrain.combine()
        self.terrain.collider = 'mesh'
        self.terrain.texture = "textures/grass"
    
    def generate_chunk(self):
        player_pos_x, player_pos_y, player_pos_z = self.player.position
        for i in range(self.chunk_width ** 2):
            x = self.chunks[i].x = floor((i / self.chunk_width) + player_pos_x - 0.5 * self.chunk_width)
            z = self.chunks[i].z = floor((i % self.chunk_width) + player_pos_z - 0.5 * self.chunk_width)
            self.chunks[i].y = floor((self.noise([x / self.freq, z / self.freq])) * self.amp)

            self.chunks[i].visible = False
    
    def generate_subset(self):
        if self.current_subset >= len(self.subsets):
            self.finish_terrain()
            return
        
        for i in range(self.sub_width):
            x = self.subcubes[i].x = floor((i + self.subcube_index) / self.terrain_width)
            z = self.subcubes[i].z = floor((i + self.subcube_index) % self.terrain_width)
            y = self.subcubes[i].y = floor((self.noise([x / self.freq, z / self.freq])) * self.amp)
<<<<<<< HEAD
            
            self.subcubes[i].parent = self.subsets[self.current_subset]
            self.subcubes[i].color = self.set_block_color(y)
=======

            self.subcubes[i].region = settings.REGIONS_LAYOUT[int(x)][int(z)]
            self.subcubes[i].parent = self.subsets[self.current_subset]
            self.subcubes[i].color = self.set_block_color(self.subcubes[i], False)
>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a
            self.subcubes[i].visible = False

            #parse_terrain.place_weird_veg(self.subcubes[i])
            #parse_terrain.place_clouds(self.subcubes[i])


        self.subsets[self.current_subset].combine(auto_destroy=False)
<<<<<<< HEAD
        #self.subsets[self.current_subset].texture = "textures/black_cube"
        #self.subsets[self.current_subset].shader = lit_with_shadows_shader
        self.subcube_index += self.sub_width
        self.current_subset += 1
    
    def set_block_color(self, y):
        cloud = 255, 255, 255
        ice = 58, 146, 194
        rock = 50, 52, 54
        lava = 194, 74, 58
        grass = 66, 110, 48
        dirt = 59, 39, 36
            
        if y > 2: r, g, b = dirt
        elif y >= 0: r, g, b = grass
        elif y > -5: r, g, b = rock
        else: r, g, b = lava

        if (r, g, b) not in (cloud, rock):
            r, g, b = [random.randint(v-5, v+5) for v in (r, g, b)]
=======
        self.subsets[self.current_subset].texture = "textures/basic"
        self.subcube_index += self.sub_width
        self.current_subset += 1
    
    def set_block_color(self, cube, mod =True):
        cloud = parse_terrain.modify_color("cloud", cube.region, mod)
        ice = parse_terrain.modify_color("ice", cube.region, mod)
        rock = parse_terrain.modify_color("rock", cube.region, mod)
        lava = parse_terrain.modify_color("lava", cube.region, mod)
        grass = parse_terrain.modify_color("grass", cube.region, mod)
        dirt = parse_terrain.modify_color("dirt", cube.region, mod)
            
        if cube.y > 2: r, g, b, alpha = dirt
        elif cube.y >= 0: r, g, b, alpha = grass
        elif cube.y > -8: r, g, b, alpha = rock
        else: r, g, b, alpha = lava

        if (r, g, b) not in (cloud, rock):
            r, g, b = [random.randint(int(v)-5, int(v)+5) for v in (r, g, b)]
>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a
        elif (r, g, b) == rock:
            m = random.randint(-5, 5)
            r, g, b = r + m, g + m, b + m

<<<<<<< HEAD
        return color.rgb(r, g, b)
=======
        return color.rgb(r, g, b, alpha)
>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a

    def finish_terrain(self):
        if not self.terrain_finished:
            self.player.disable()
            self.terrain.combine()
            self.terrain_finished = True
<<<<<<< HEAD
            self.terrain.texture = "textures/black_cube"
            self.sky.combine()
=======
            self.player.x = floor(settings.TERRAIN_WIDTH/2)
            self.player.z = floor(settings.TERRAIN_WIDTH/2)
            self.player.y = 100
>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a
            self.player.enable()
    
    def n_map(self, n, min1, max1, min2, max2):
        return ((n - min1) / (max1 - min1)) * (max2 - min2) + min2

<<<<<<< HEAD
    def place_smiling_orb(self):
        for i in range(settings.STARS_AMOUNT):
            xx = random.randint(1, self.terrain_width)
            z = random.randint(1, self.terrain_width)
            y = random.randint(0, 5)
            r, g, b = [random.randint(0, 255) for _ in range(3)]
            
            e = Entity(
                   parent = self.sky,
                   model="models/mist_orb",
                   color = color.rgb(r, g, b),
                    x = xx,
                    z = z,
                    y = y,
                    scale = 1 #random.randint(1, 10) / 100
                    )
            self.stars.append(e)

=======
>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a
    def update_stars_position(self):
        mod = 0.01
        if self.sky.x >= 5: self.movement_direction = -1
        if 0 < self.sky.x < 5: self.movement_direction = -1
        
        self.sky.x += (0.01 * self.movement_direction)
<<<<<<< HEAD
=======

    def falling_rock(self):
       x = random.randint(1, self.terrain_width)
       z = random.randint(1, self.terrain_width)
       y = random.randint(20, 500)

       for x in range(100):
            e = Block(
                parent = self.sky,
                model = "models/mist_orb",
                collider = None,
                scale = settings.STARS_SCALE,
                position = ()
            )

            self.stars.append(e)
    def update_rock(self):
        for entity in self.stars:
            if entity.y == -self.amp:
                entity.y = random.randint(50, 100)
                entity.x = random.randint(0, self.terrain_width)
                entity.z = random.randint(0, self.terrain_width)
            else:
                entity.y -= 0.5

>>>>>>> be99711d67f0ed8897551e994f131bb42b32b94a

