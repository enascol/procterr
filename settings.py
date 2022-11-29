from numpy import floor

import random

BLOCK_ALPHA = 255
TERRAIN_WIDTH = 255
MIDDLE_X = MIDDLE_Z = floor(TERRAIN_WIDTH/2)
AMP = 30
FREQUENCY = 45
OCTAVE = 1
SEED = random.randint(1, 50000)
FOG_DENSITY = 0
FOG_COLOR = 0, 0, 0

WEIRD_VEG_PROBABILITY = 10

STARS_AMOUNT = 500
STARS_SCALE = 0.3

with open("D:\Python\procga\level", "r") as lf:
    REGIONS_LAYOUT = [line.strip() for line in lf.readlines()]

FOG_DENSITY = 0
FOG_COLOR = 255, 0, 0

STARS_AMOUNT = 500

AUDIO_PATH = r"D:\Python\procga\audio"

REGIONS_COLOR = {}

FLOOR = 50
CEIL = 100

for x in range(4):
    REGIONS_COLOR[str(x + 1)] = {
        "cloud": [random.randint(0, 255) for x in range(3)] + [BLOCK_ALPHA],
        "ice": [random.randint(FLOOR, CEIL) for x in range(3)] + [BLOCK_ALPHA],
        "rock": [random.randint(FLOOR, CEIL) for x in range(3)] + [BLOCK_ALPHA],
        "lava": [random.randint(FLOOR, CEIL) for x in range(3)] + [BLOCK_ALPHA],
        "grass": [random.randint(FLOOR, CEIL) for x in range(3)] + [BLOCK_ALPHA],
        "dirt": [random.randint(FLOOR, CEIL) for x in range(3)] + [BLOCK_ALPHA],
        }
