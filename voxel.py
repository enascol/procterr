from ursina import *
from ursina.shaders import lit_with_shadows_shader

import sounds
import blocks

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), parent =scene, block_name="grass", model =None, **arg):
        self.block_name = block_name
        settings = blocks.SETTINGS[self.block_name]
        self.value = random.randint(1, 100)

        super().__init__(
            parent = parent,
            position = position,
            model = model,
            texture = settings["texture"] or "textures/no_texture",
            color = color.color(0, 0, 1),
            origin_x = 0.5,
            scale = 0.5,
            shader = lit_with_shadows_shader,
            **arg
        )

        self.placing = settings["sounds"]["placing"] or "placing"
        self.destroying = settings["sounds"]["destroying"] or "destroying"

    def input(self, key):
        if self.hovered:
            if self.block_name == "invisible wall":
                pass
            else:
                if key == "left mouse down":
                    Voxel(position=self.position + mouse.normal)
                    sounds.play(self.placing)
                elif key == "right mouse down":
                    destroy(self)
                    sounds.play(self.destroying, volume=10)
