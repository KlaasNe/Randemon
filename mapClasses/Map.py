import random
from mapClasses import *


class Map:

    def __init__(self, chunk_nb_h, chunk_nb_v, chunk_size):
        self.chunk_size = chunk_size
        self.chunk_nb_h = chunk_nb_h
        self.chunk_nb_v = chunk_nb_v
        self.chunks = [[Chunk(chunk_size)] * chunk_nb_h] * chunk_nb_v
        for y in range(chunk_size):
            for x in range(chunk_size):
                self.chunks[0][0].get_layer("GROUND0").set_tile(x, y, Tile("NATURE", 0, random.randint(0, 7)))
