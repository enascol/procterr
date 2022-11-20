from ursina import *

class Sky(Entity):

    def __init__(self, texture):
        super().__init__(
            parent = scene,
            model = "sphere",
            texture = texture
        )