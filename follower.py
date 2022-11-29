from ursina import *

class Pet(Entity):

    def __init__(self, player, **config):
        super().__init__(
            parent = player,
            model = "cube",
            texture = "textures/basic",
            collider = None,
            position = (player.x, player.z, player.y + 5)
        )

        self.player = player
    
    def update_position(self):
        self.x = self.player.x
        self.z = self.player.z
        self.y = self.player.y + 5
