from ursina import *

class Sun():

    def __init__(self, **config):
        self.sun = DirectionalLight(**config)
        self.x = 1
        self.y = -1
        self.z = -1
        self.look()


    def look(self):
        self.sun.look_at(Vec3(self.x, self.y, self.z))

    def update_look_direction(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z
        self.sun.look_at(Vec3(self.x, self.y, self.z))
        