from enum import Enum


class TileWeights(Enum):
    PATH = -2
    GRASS = 8
    HILL = 64
    WATER = 8
    IMPASSABLE = 999999
