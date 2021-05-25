from mapClasses import *


class Map:

    def __init__(self, chunk_nb_h, chunk_nb_v, chunk_size_x, chunk_size_y):
        self.chunks = [[Chunk(chunk_size_x, chunk_size_y)] * chunk_nb_h] * chunk_nb_v
