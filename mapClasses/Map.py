import random

from generators.waterGenerator import *
from mapClasses import *


class Map:

    def __init__(self, chunk_nb_h, chunk_nb_v, chunk_size):
        self.chunk_size = chunk_size
        self.chunk_nb_h = chunk_nb_h
        self.chunk_nb_v = chunk_nb_v
        off_x, off_y = random.randint(0, 1000000), random.randint(0, 1000000)
        self.chunks = [[Chunk(chunk_size, off_x + x, off_y + y) for x in range(chunk_nb_h) for y in range(chunk_nb_v)] * chunk_nb_h] * chunk_nb_v
        # for y in range(chunk_size):
        #     for x in range(chunk_size):
        #         self.chunks[0][0].get_layer("GROUND0").set_tile(x, y, Tile("NATURE", 0, random.randint(0, 7)))
        create_rivers(self.chunks[0][0])
