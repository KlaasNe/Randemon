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
        random.seed(seed)
        self.chunk_size = chunk_size
        self.chunk_nb_h = chunk_nb_h
        self.chunk_nb_v = chunk_nb_v
        off_x, off_y = random.randint(0, 1000000), random.randint(0, 1000000)
        self.chunks = [[Chunk(chunk_size, off_x + x, off_y + y) for x in range(chunk_nb_h) for y in range(chunk_nb_v)] * chunk_nb_h] * chunk_nb_v
        for y in range(chunk_nb_v):
            for x in range(chunk_nb_h):
                create_rivers(self.chunks[y][x])
                create_edges(self.chunks[y][x], 0)
                # spawn_functional_buildings(self.chunks[y][x], "p1")
                for building in BuildingTypes:
                    spawn_building(self.chunks[y][x], building.value, "p1")
                draw_path2(self.chunks[y][x], 0)
                create_path(self.chunks[y][x])
                create_trees(self.chunks[y][x], 0.55, off_x, off_y)
                grow_grass(self.chunks[y][x], 0.6, off_x, off_y)
        print("seed=" + str(seed))
