import random
import sys

from buildings.BuildingTypes import BuildingTypes
from generators.buildingGenerator import *
from generators.hillGenerator import *
from generators.plantGenerator import *
from generators.waterGenerator import *
from generators.pathGenerator import *
from mapClasses import *


class Map:

    def __init__(self, chunk_nb_h, chunk_nb_v, chunk_size, seed=random.randint(0, sys.maxsize)):
        self.chunk_size = chunk_size
        self.chunk_nb_h = chunk_nb_h
        self.chunk_nb_v = chunk_nb_v
        self.seed = seed
        random.seed(self.seed)
        print("seed=" + str(self.seed))
        off_x, off_y = random.randint(0, 1000000), random.randint(0, 1000000)
        self.chunks = [[Chunk(self, chunk_size, x, y, off_x + x * self.chunk_size, off_y + y * self.chunk_size) for x in range(chunk_nb_h)] for y in range(chunk_nb_v)]
        for y in range(chunk_nb_v):
            for x in range(chunk_nb_h):
                current_chunk = self.chunks[y][x]
                create_rivers(current_chunk)
                create_edges(current_chunk, 0)
                if random.randint(0, 0) == 0:
                    for building in BuildingTypes:
                        spawn_building(current_chunk, building.value, "p1")
                draw_path2(current_chunk, 0)
                create_path(current_chunk)
                create_trees(current_chunk, 0.55)
                grow_grass(current_chunk, 0.6)

    def get_chunk(self, x, y):
        try:
            return self.chunks[y][x]
        except IndexError:
            return None
