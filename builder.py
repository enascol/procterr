from ursina import *

class BuilderTool(Entity):

    def __init__(self, **config):
        super().__init__(
            texture = "textures/follower",
            model = "cube",            
            **config
            )
        self.distance = 2
    
    def select(self, player):
        self.position = round(player.position + camera.forward * self.distance)
        self.y += 2

        self.y = round(self.y)
        self.x = round(self.x)
        self.z = round(self.z)
    
    def place(self):
        block = duplicate(self)
        block.collider = "cube"
        block.model = "cube"
