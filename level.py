from ursina import *
from voxel import Voxel
from settings import TERRAIN_WIDTH
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
        self.noise = PerlinNoise(octaves = 1, seed = random.randint(1, 50000))
        self.freq = 30
        self.amp = 30

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

            if y > 5:
                c = color.rgb(50, 168, 135)
            elif y < -10:
                c = color.rgb(x * 10, y * 10, z * 10)
            elif y < -8:
                c = color.rgb(168, 72, 50)
            elif y < -2:
                c = color.rgb(100, 102, 100)
            else:
                c = color.rgb(64, 168, 50)

            self.subcubes[i].parent = self.subsets[self.current_subset]
            self.subcubes[i].color = c
            self.subcubes[i].visible = False
        
        self.subsets[self.current_subset].combine(auto_destroy=False)
        self.subsets[self.current_subset].texture = "textures/centered_white_spiral"
        self.subcube_index += self.sub_width
        self.current_subset += 1
    
    def finish_terrain(self):
        if not self.terrain_finished:
            application.pause()
            self.terrain.combine()
            self.terrain_finished = True
            self.player.x = int(self.terrain.x / 2)
            self.player.y = 20
            application.resume()

