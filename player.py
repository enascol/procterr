from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from settings import TERRAIN_WIDTH
from follower import Pet
 
class Player(FirstPersonController):

    def __init__(self, **config):
        super().__init__(**config)


            