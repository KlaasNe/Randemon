from enum import Enum


class TileWeights(Enum):
    PATH = -8
    GRASS = 8
    HILL = 16
    WATER = 32
    IMPASSABLE = 999999
