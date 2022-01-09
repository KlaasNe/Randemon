from enum import Enum


class TileWeights(Enum):
    PATH = -1
    GRASS = 8
    HILL = 16
    WATER = 64
    IMPASSABLE = 999999
