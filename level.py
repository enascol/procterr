from ursina import *
from voxel import Voxel
from settings import TERRAIN_WIDTH, FREQUENCY, AMP, OCTAVE
from perlin_noise import PerlinNoise
from numpy import floor
from ursina.shaders import lit_with_shadows_shader

class Level:

    def __init__(self, player):
        self.player = player 

        # Terrain info
        self.terrain_width = TERRAIN_WIDTH
        self.terrain = Entity(model = None, collider =None)
        self.terrain_finished = False

        # Procedural generation params
        self.noise = PerlinNoise(octaves = OCTAVE, seed = random.randint(1, 50000))
        self.freq = FREQUENCY
        self.amp = AMP

        # Terrain chunk settings
        # This terrain is small enough to be walked on
        # and will be only rendered as you walk.
        # Its also invisible
        self.chunk_width = 6
        self.chunks = [Entity(model = "cube", collider = "box") for _ in range(self.chunk_width ** 2)]

        # Subsets settings
        # This is the visible terrain
        # Its faster to load since wont have a collision mesh
        self.sub_width = self.terrain_width
        self.subcube_index = 0
        self.current_subset = 0
        self.subcubes = [Entity(model = "cube") for _ in range(self.sub_width)]
        self.subsets = [Entity(model = None) for _ in range(int((self.terrain_width ** 2) / self.sub_width))]

        self.place_smiling_orb()

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
            
            self.subcubes[i].parent = self.subsets[self.current_subset]
            self.subcubes[i].color = self.set_block_color(y)
            self.subcubes[i].visible = False

        self.subsets[self.current_subset].combine(auto_destroy=False)
        #self.subsets[self.current_subset].texture = "textures/black_cube"
        self.subcube_index += self.sub_width
        self.current_subset += 1
    
    def set_block_color(self, y):
            cloud = 255, 255, 255
            ice = 58, 146, 194
            rock = 50, 52, 54
            lava = 194, 74, 58
            grass = 97, 194, 58
            dirt = 59, 39, 36
            
            if y > 8:
                r, g, b = cloud
            elif y > 6:
                r, g, b = ice
            elif y > 4:
                r, g, b = dirt
            elif y > 6:
                r, g, b = ice
            elif y < -6:
                r, g, b = lava
            elif y < -2:
                r, g, b = rock
            else:
                r, g, b = grass
            
            if (r, g, b) not in (cloud, rock):
                r, g, b = [random.randint(v-5, v+5) for v in (r, g, b)]
            elif (r, g, b) == rock:
                m = random.randint(-5, 5)
                r, g, b = r + m, g + m, b + m
            
            return color.rgb(r, g, b)

    def finish_terrain(self):
        if not self.terrain_finished:
            self.terrain.combine()
            self.terrain_finished = True
            self.terrain.texture = "textures/black_cube"
    
    def n_map(self, n, min1, max1, min2, max2):
        return ((n - min1) / (max1 - min1)) * (max2 - min2) + min2

    def place_smiling_orb(self):
        for x in range(100):
            Entity(model="models/smiling_orb", 
                  texture="textures/smile",
                    x = random.randint(1, self.terrain_width),
                    z = random.randint(1, self.terrain_width),
                    y = 10
                    )

