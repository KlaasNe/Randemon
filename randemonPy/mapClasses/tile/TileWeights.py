from enum import Enum


class TileWeights(Enum):
    PATH = -8
    GRASS = 1
    HILL = 8
    WATER = 1
    IMPASSABLE = 999999
