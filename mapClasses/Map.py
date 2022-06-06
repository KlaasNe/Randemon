import random
import sys
from colorama import Fore
from colorama import Style

from buildings.BuildingTypes import BuildingTypes
from generators.buildingGenerator import *
from generators.hillGenerator import *
from generators.plantGenerator import *
from generators.pokemonGenerator import spawn_pokemons
from generators.waterGenerator import *
from generators.pathGenerator import *
from generators.heightMapGenerator import *
from mapClasses import *

from alive_progress import alive_bar


class Map:

    def __init__(self, chunk_nb_h, chunk_nb_v, chunk_size, max_buildings=16, island=False, strict=True, seed=random.randint(0, sys.maxsize), height_map=False):
        self.chunk_size = chunk_size
        self.chunk_nb_h = chunk_nb_h
        self.chunk_nb_v = chunk_nb_v
        self.size_h = self.chunk_size * self.chunk_nb_h
        self.size_v = self.chunk_size * self.chunk_nb_v
        self.seed = seed
        random.seed(self.seed)
        print(Fore.LIGHTBLUE_EX + "seed = " + Fore.LIGHTYELLOW_EX + str(self.seed) + Style.RESET_ALL)
        print("Creating terrain...")
        off_x, off_y = random.randint(0, 1000000), random.randint(0, 1000000)
        self.height_map = generate_height_map(self.chunk_size * self.chunk_nb_h, self.chunk_size * self.chunk_nb_v, 5, off_x, off_y)
        # self.height_map = generate_height_map_from_image("heightMaps/heartHeight.png")
        if island:
            custom_height_map_mask = [-4, -3, -2, -1, 0, 1, 0, -1, -2]  # left to right -> outside to center
            add_island_mask(self, 5, off_x, off_y, strict=strict)
            smooth_height(self, radius=5)
        self.chunks = [[Chunk(self, chunk_size, x, y, off_x + x * self.chunk_size, off_y + y * self.chunk_size) for x in range(chunk_nb_h)] for y in range(chunk_nb_v)]
        with alive_bar(self.chunk_nb_v * self.chunk_nb_h, title="Generating chunks", theme="classic") as chunk_bar:
            for y in range(chunk_nb_v):
                for x in range(chunk_nb_h):
                    chunk_bar()
                    current_chunk = self.chunks[y][x]
                    if not height_map:
                        if island:
                            remove_faulty_heights(current_chunk)
                        create_edges(current_chunk, 0)
                        create_rivers(current_chunk, 1)
                        if max_buildings > 0 and random.randint(0, 3) <= 1:
                            current_chunk.has_town = True
                            path_type = random.randint(0, 7)
                            valid_town = spawn_functional_buildings(current_chunk)
                            if valid_town:
                                for b in range(max_buildings):
                                    spawn_building(current_chunk, BuildingTypes["H" + str(random.randint(0, 21))].value)
                                draw_path2(current_chunk)
                                create_path(current_chunk, path_type)
                            else:
                                current_chunk.has_town = False
                                current_chunk.clear_layer("BUILDINGS")
                                remove_path(current_chunk)

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

    def change_height(self, chunk, x, y, val):
        cx, cy = chunk.chunk_x, chunk.chunk_y
        self.height_map[cy * self.chunk_size + y - 1][cx * self.chunk_size + x - 1] += val


