from enum import Enum


class TileWeights(Enum):
    PATH = -8
    GRASS = 8
    HILL = 32
    WATER = 64
    IMPASSABLE = 999999
