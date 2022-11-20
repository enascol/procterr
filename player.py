from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import sounds
 
class Player(FirstPersonController):

    def __init__(self, **config):
        super().__init__(**config)


            