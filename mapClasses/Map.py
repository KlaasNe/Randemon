import random
import sys

from buildings.BuildingTypes import BuildingTypes
from generators.buildingGenerator import *
from generators.hillGenerator import *
from generators.plantGenerator import *
from generators.pokemonGenerator import spawn_pokemons
from generators.waterGenerator import *
from generators.pathGenerator import *
from generators.heightMapGenerator import *
from mapClasses import *


class Map:

    def __init__(self, chunk_nb_h, chunk_nb_v, chunk_size, max_buildings=16, island=True, seed=random.randint(0, sys.maxsize), height_map=False):
        self.chunk_size = chunk_size
        self.chunk_nb_h = chunk_nb_h
        self.chunk_nb_v = chunk_nb_v
        self.size_h = self.chunk_size * self.chunk_nb_h
        self.size_v = self.chunk_size * self.chunk_nb_v
        self.seed = seed
        random.seed(self.seed)
        print("seed=" + str(self.seed))
        off_x, off_y = random.randint(0, 1000000), random.randint(0, 1000000)
        self.height_map = generate_height_map(self.chunk_size * self.chunk_nb_h, self.chunk_size * self.chunk_nb_v, 5, off_x, off_y)
        if island:
            add_island_mask(self, -4, 4)
            smooth_height(self)
        self.chunks = [[Chunk(self, chunk_size, x, y, off_x + x * self.chunk_size, off_y + y * self.chunk_size) for x in range(chunk_nb_h)] for y in range(chunk_nb_v)]
        for y in range(chunk_nb_v):
            for x in range(chunk_nb_h):
                current_chunk = self.chunks[y][x]
                if not height_map:
                    create_rivers(current_chunk)
                    create_edges(current_chunk, 0)
                    if max_buildings > 0 and random.randint(0, 3) <= 1:
                        current_chunk.has_town = True
                        path_type = random.randint(0, 7)
                        spawn_functional_buildings(current_chunk)
                        for b in range(max_buildings):
                            spawn_building(current_chunk, BuildingTypes["H" + str(random.randint(0, 21))].value)
                        draw_path2(current_chunk)
                        create_path(current_chunk, path_type)

                    spawn_pokemons(current_chunk)
                    create_trees(current_chunk, 0.55)
                    grow_grass(current_chunk, 0.6)
                else:
                    draw_height_map(self, current_chunk)

    def get_chunk(self, x, y):
        try:
            return self.chunks[y][x]
        except IndexError:
            return None

    def get_height(self, chunk, x, y):
        cx, cy = chunk.chunk_x, chunk.chunk_y
        try:
            return self.height_map[cy * self.chunk_size + y - 1][cx * self.chunk_size + x - 1]
        except Exception as e:
            print(e, cy * self.chunk_size + y, cx * self.chunk_size + x)
