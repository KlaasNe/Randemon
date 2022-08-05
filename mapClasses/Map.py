import random
import sys
from colorama import Fore
from colorama import Style
from typing import Optional

from buildings.BuildingTheme import BuildingTheme
from buildings.BuildingTypes import BuildingTypes
from buildings.BuildingTypes import BuildingThemes
from generators.buildingGenerator import *
from generators.hillGenerator import *
from generators.plantGenerator import *
from generators.pokemonGenerator import spawn_pokemons
from generators.waterGenerator import *
from generators.pathGenerator import *
from generators.heightMapGenerator import *
from mapClasses import Chunk

from alive_progress import alive_bar


class Map:

    def __init__(self, chunk_nb_h, chunk_nb_v, chunk_size, max_buildings=16, island=False, seed=random.randint(0, sys.maxsize), height_map=False, themed_towns=False) -> None:
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
        self.height_map = generate_height_map(self.chunk_size * self.chunk_nb_h, self.chunk_size * self.chunk_nb_v, 5, off_x, off_y, additional_noise_maps=3, island=island)
        # self.height_map = generate_height_map_from_image("heightMaps/earthLandMassHeight.png")
        smooth_height(self, radius=5)
        self.chunks = [[Chunk(self.height_map, chunk_size, x, y, off_x + x * self.chunk_size, off_y + y * self.chunk_size) for x in range(chunk_nb_h)] for y in range(chunk_nb_v)]
        self.lake_tiles = set()
        self.sea_tiles = set()
        with alive_bar(self.chunk_nb_v * self.chunk_nb_h, title="Removing faulty heights", theme="classic") as faulty_heights_bar:
            for y in range(chunk_nb_v):
                for x in range(chunk_nb_h):
                    current_chunk = self.chunks[y][x]
                    remove_faulty_heights(current_chunk, force=True)
                    faulty_heights_bar()
        create_lakes_and_sea(self)
        with alive_bar(self.chunk_nb_v * self.chunk_nb_h, title="Generating chunks", theme="classic") as chunk_bar:
            for y in range(chunk_nb_v):
                for x in range(chunk_nb_h):
                    current_chunk = self.chunks[y][x]
                    if not height_map:
                        create_edges(current_chunk, 0)
                        create_rivers(current_chunk, self.lake_tiles)
                        if max_buildings > 0 and random.randint(0, 3) <= 1:
                            current_chunk.has_town = True
                            path_type = random.randint(0, 7)
                            valid_town = spawn_functional_buildings(current_chunk)
                            if valid_town:
                                if themed_towns:
                                    building_theme: BuildingTheme = BuildingThemes.get_random_theme().value
                                for b in range(max_buildings):
                                    if themed_towns:
                                        spawn_building(current_chunk, building_theme.get_random_building_type().value)
                                    else:
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
                    chunk_bar()

    def get_chunk(self, x: int, y: int) -> Optional[Chunk]:
        try:
            return self.chunks[y][x]
        except IndexError:
            return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size_h and 0 <= y < self.size_v

    def get_height_raw_pos(self, x: int, y: int) -> int:
        try:
            return self.height_map[y][x]
        except IndexError as e:
            return 0

    def get_height(self, c: Chunk, x: int, y: int) -> int:
        cx, cy = c.chunk_x, c.chunk_y
        x_raw, y_raw = cx * self.chunk_size + x, cy * self.chunk_size + y
        if self.in_bounds(x_raw, y_raw):
            return self.get_height_raw_pos(x_raw, y_raw)
        else:
            return 0

    def change_height(self, c: Chunk, x: int, y: int, val: int) -> None:
        cx, cy = c.chunk_x, c.chunk_y
        self.height_map[cy * self.chunk_size + y][cx * self.chunk_size + x] += val
