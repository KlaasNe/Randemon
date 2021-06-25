from enum import Enum


class TileWeights(Enum):
    PATH = 0
    GRASS = 8
    HILL = 32
    WATER = 16
    IMPASSABLE = 999999
