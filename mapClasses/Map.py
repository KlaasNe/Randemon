import random
import sys
from colorama import Fore
from colorama import Style
from typing import Optional, Iterator

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

    def __init__(self,
                 chunk_nb_h: int,
                 chunk_nb_v: int,
                 chunk_size: int,
                 max_buildings: int = 16,
                 island: bool = False,
                 seed: int = random.randint(0, sys.maxsize),
                 height_map: bool = False,
                 themed_towns: bool = False) -> None:
        self.chunk_size: int = chunk_size
        self.chunk_nb_h: int = chunk_nb_h
        self.chunk_nb_v: int = chunk_nb_v
        self.size_h: int = self.chunk_size * self.chunk_nb_h
        self.size_v: int = self.chunk_size * self.chunk_nb_v
        self.seed: int = seed
        random.seed(self.seed)
        print(Fore.LIGHTBLUE_EX + "seed = " + Fore.LIGHTYELLOW_EX + str(self.seed) + Style.RESET_ALL)
        print("Creating terrain...")
        off_x, off_y = random.randint(0, 1000000), random.randint(0, 1000000)
        self.height_map: list[list[int]] = generate_height_map(self.chunk_size * self.chunk_nb_h, self.chunk_size * self.chunk_nb_v, 5, off_x, off_y, additional_noise_maps=3, island=island)
        # self.height_map = generate_height_map_from_image("heightMaps/earthLandMassHeight.png")
        smooth_height(self, radius=5)
        self.chunks: list[list[Chunk]] = [[Chunk(self.height_map, chunk_size, x, y, off_x + x * self.chunk_size, off_y + y * self.chunk_size) for x in range(chunk_nb_h)] for y in range(chunk_nb_v)]
        self.lake_tiles: set[tuple] = set()
        self.sea_tiles: set[tuple] = set()
        water_threshold = 2
        with alive_bar(self.chunk_nb_v * self.chunk_nb_h, title="Removing faulty heights", theme="classic") as faulty_heights_bar:
            for y in range(chunk_nb_v):
                for x in range(chunk_nb_h):
                    current_chunk = self.chunks[y][x]
                    remove_faulty_heights(current_chunk, force=True)
                    faulty_heights_bar()
        create_lakes_and_sea(self)
        create_beach(self, water_threshold)  # TODO dont do create beach twice
        with alive_bar(self.chunk_nb_v * self.chunk_nb_h, title="Generating chunks", theme="classic") as chunk_bar:
            for y in range(chunk_nb_v):
                for x in range(chunk_nb_h):
                    current_chunk = self.chunks[y][x]
                    if not height_map:
                        create_edges(current_chunk, hill_type=0)
                        # create_rivers(current_chunk, self.lake_tiles)
                        if max_buildings > 0 and random.randint(0, 3) <= 1:
                            path_type = random.randint(0, 7)
                            current_chunk.has_town = True
                            valid_town = spawn_functional_buildings(current_chunk, path_type)
                            if valid_town:
                                if themed_towns:
                                    building_theme: BuildingTheme = BuildingThemes.get_random_theme().value
                                for b in range(random.randint(1, max_buildings)):
                                    if themed_towns:
                                        spawn_building(current_chunk, building_theme.get_random_building_type().value, path_type)
                                    else:
                                        spawn_building(current_chunk, BuildingTypes["H" + str(random.randint(0, 21))].value, path_type)
                                draw_path2(current_chunk, path_type)
                            else:
                                current_chunk.has_town = False
                                current_chunk.clear_layer("BUILDINGS")
                                remove_path(current_chunk)
                    else:
                        draw_height_map(self, current_chunk)
                    chunk_bar()

        if not height_map:
            create_beach(self, water_threshold)
            create_path(self)

            with alive_bar(self.chunk_nb_v * self.chunk_nb_h, title="Updating chunks (nature, sea and plants and stuff)", theme="classic") as chunk_bar:
                for y in range(chunk_nb_v):
                    for x in range(chunk_nb_h):
                        current_chunk = self.chunks[y][x]
                        create_rivers(current_chunk, self.lake_tiles, water_threshold)
                        spawn_pokemons(current_chunk)
                        create_trees(current_chunk, 0.55)
                        grow_grass(current_chunk, 0.6)
                        chunk_bar()

    def __iter__(self) -> Iterator[Chunk]:
        for chunk_row in self.chunks:
            for chunk in chunk_row:
                yield chunk

    def get_chunk(self, x: int, y: int) -> Optional[Chunk]:
        try:
            return self.chunks[y][x]
        except IndexError:
            return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size_h and 0 <= y < self.size_v

    def parse_chunk_coordinate(self, c: Chunk, x: int, y: int) -> tuple[int, int]:
        cx, cy = c.chunk_x, c.chunk_y
        x_parsed, y_parsed = cx * self.chunk_size + x, cy * self.chunk_size + y
        return x_parsed, y_parsed

    def parse_to_chunk_coordinate(self, x: int, y: int) -> tuple[Chunk, int, int]:
        cx, cy = x // self.chunk_size, y // self.chunk_size
        x_parsed, y_parsed = x % self.chunk_size, y % self.chunk_size
        return self.get_chunk(cx, cy), x_parsed, y_parsed

    def get_height_parsed_pos(self, x: int, y: int) -> int:
        try:
            return self.height_map[y][x]
        except IndexError as e:
            return 0

    def get_height(self, c: Chunk, x: int, y: int) -> int:
        x_parsed, y_parsed = self.parse_chunk_coordinate(c, x, y)
        if self.in_bounds(x_parsed, y_parsed):
            return self.get_height_parsed_pos(x_parsed, y_parsed)
        else:
            return 0

    def change_height(self, c: Chunk, x: int, y: int, val: int) -> None:
        x_parsed, y_parsed = self.parse_chunk_coordinate(c, x, y)
        self.height_map[y_parsed][x_parsed] += val
