import random

from generators.hillGenerator import *
from generators.plantGenerator import *
from generators.waterGenerator import *
from mapClasses import *


class Map:

    def __init__(self, chunk_nb_h, chunk_nb_v, chunk_size):
        self.chunk_size = chunk_size
        self.chunk_nb_h = chunk_nb_h
        self.chunk_nb_v = chunk_nb_v
        off_x, off_y = random.randint(0, 1000000), random.randint(0, 1000000)
        self.chunks = [[Chunk(chunk_size, off_x + x, off_y + y) for x in range(chunk_nb_h) for y in range(chunk_nb_v)] * chunk_nb_h] * chunk_nb_v
        for y in range(chunk_nb_v):
            for x in range(chunk_nb_h):
                create_rivers(self.chunks[y][x])
                create_edges(self.chunks[y][x])
                create_trees(self.chunks[y][x], 0.55, off_x, off_y)
                grow_grass(self.chunks[y][x], 0.6, off_x, off_y)
