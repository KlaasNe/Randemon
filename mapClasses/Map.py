from random import random

from hkb_diamondsquare import DiamondSquare as ds
from colorama import Fore
from colorama import Style
from typing import Optional, Iterator

from buildings.BuildingTheme import BuildingTheme
from buildings.BuildingTypes import BuildingThemes
from generators.pokemonGenerator import spawn_pokemons
from generators.heightMapGenerator import *
from generators.buildingGenerator import *
from generators.hillGenerator import *
from generators.pathGenerator import *
from generators.plantGenerator import *
from generators.townMapGenerator import draw_town_map, generate_town_map
from generators.waterGenerator import *
from mapClasses import Chunk

from alive_progress import alive_bar


class Map:

    def __init__(self,
                 chunk_nb_h: int,
                 chunk_nb_v: int,
                 chunk_size: int,
                 seed: int,
                 max_buildings: int = 16,
                 island: bool = False,
                 make_height_map: bool = False,
                 themed_towns: bool = True,
                 terrain_chaos: int = 4,
                 max_height: int = 6,
                 town_map: str = None,
                 style: str = "squareDiamond") -> None:

        self.chunk_size: int = chunk_size
        self.chunk_nb_h: int = chunk_nb_h
        self.chunk_nb_v: int = chunk_nb_v
        self.size_h: int = self.chunk_size * self.chunk_nb_h
        self.size_v: int = self.chunk_size * self.chunk_nb_v
        self.max_buildings = max_buildings
        self.seed: int = seed
        self.draw_height_map = make_height_map
        self.themed_towns = themed_towns
        self.max_height = max_height
        random.seed(self.seed)
        print(Fore.LIGHTBLUE_EX + "seed = " + Fore.LIGHTYELLOW_EX + str(self.seed) + Style.RESET_ALL)
        print("Creating terrain...")
        off_x, off_y = random.randint(0, 10000000), random.randint(0, 10000000)
        if style == "simplex":
            self.height_map: list[list[int]] = generate_height_map(
                self.size_h,
                self.size_v, self.max_height,
                off_x, off_y, self.chunk_size,
                additional_noise_maps=1, island=island,
                terrain_chaos=terrain_chaos
                )
        elif style == "squareDiamond":
            self.height_map: list[list[int]] = ds.diamond_square(
                shape=(self.size_h, self.size_v),
                min_height=-max_height,
                max_height=max_height,
                roughness=0.55,
                random_seed=seed
            )
            for y in range(self.chunk_size * self.chunk_nb_v):
                for x in range(self.chunk_size * self.chunk_nb_h):
                    self.height_map[y][x] += plateau((x - (self.size_h // 2)) / (self.size_h / 2),
                                                     (y - (self.size_v // 2)) / (self.size_v / 2), 0.15, 1, 0.5)
                    self.height_map[y][x] = max(0, self.height_map[y][x])
        # self.height_map = generate_height_map_from_image("heightMaps/earthLandMassHeight.png")
        smooth_height(self)
        self.chunks: list[list[Chunk]] = [
            [Chunk(self.height_map, chunk_size, x, y, off_x + x * self.chunk_size, off_y + y * self.chunk_size) for x in
             range(chunk_nb_h)] for y in range(chunk_nb_v)]
        self.water_tiles: set[tuple[int, int]] = set()
        self.lake_tiles: set[tuple[int, int]] = set()
        self.sea_tiles: set[tuple[int, int]] = set()
        self.path_tiles: set[Coordinate] = set()
        self.beach_tiles: set[tuple[int, int]] = set()
        self.towns: set[Coordinate] = set()
        self.route_chunks: set[Coordinate] = set()
        self.town_map: str = town_map
        self.town_map_img: Image = None

    def __iter__(self) -> Iterator[Chunk]:
        for chunk_row in self.chunks:
            for chunk in chunk_row:
                yield chunk

    def create(self):
        water_threshold = 2
        max_beach_inland_depth = 16
        with alive_bar(self.chunk_nb_v * self.chunk_nb_h, title="Removing faulty heights",
                       theme="classic") as faulty_heights_bar:
            for y in range(self.chunk_nb_v):
                for x in range(self.chunk_nb_h):
                    current_chunk = self.chunks[y][x]
                    remove_faulty_heights(current_chunk, force=True)
                    faulty_heights_bar()
        # create_lakes_and_sea(self) TODO fix this
        self.beach_tiles = create_beach(self, max_beach_inland_depth, water_threshold)
        with alive_bar(self.chunk_nb_v * self.chunk_nb_h, title="Generating chunks", theme="classic") as chunk_bar:
            powerplant = False
            for y in range(self.chunk_nb_v):
                for x in range(self.chunk_nb_h):
                    current_chunk = self.chunks[y][x]
                    if not self.draw_height_map:
                        create_edges(current_chunk, hill_type=0)
                        # create_rivers(current_chunk, self.lake_tiles)
                        if self.max_buildings > 0 and current_chunk.can_have_town:
                            path_type = random.randint(0, 7)
                            if random.randint(0, 9) < 9:
                                current_chunk.has_town = True
                                valid_town = spawn_functional_buildings(self, current_chunk, path_type)
                                if valid_town:
                                    self.towns.add(Coordinate(x, y))
                                    for (cx, cy) in Coordinate(x, y).around():
                                        try:
                                            self.chunks[cy][cx].can_have_town = False
                                        except IndexError:
                                            pass
                                    if self.themed_towns:
                                        building_theme: BuildingTheme = BuildingThemes.get_random_theme().value
                                    for b in range(random.randint(1, self.max_buildings)):
                                        if self.themed_towns:
                                            spawn_building(self, current_chunk,
                                                           building_theme.get_random_building_type().value, path_type)
                                        else:
                                            spawn_building(self, current_chunk,
                                                           BuildingTypes["H" + str(random.randint(0, 21))].value,
                                                           path_type)
                                    draw_path2(self, current_chunk, path_type)
                                else:
                                    current_chunk.has_town = False
                                    current_chunk.clear_layer("BUILDINGS")
                                    remove_path(current_chunk)
                            else:
                                if not powerplant:
                                    spawn_building(self, current_chunk, BuildingTypes.POWERPLANT.value, path_type)
                    else:
                        draw_height_map(self, current_chunk)
                    chunk_bar()

        if not self.draw_height_map:
            create_path(self)

            with alive_bar(self.chunk_nb_v * self.chunk_nb_h,
                           title="Updating chunks (nature, sea and plants and stuff)", theme="classic") as chunk_bar:
                for y in range(self.chunk_nb_v):
                    for x in range(self.chunk_nb_h):
                        current_chunk = self.chunks[y][x]
                        create_rivers(current_chunk, self.lake_tiles, water_threshold, no_sprite=True)
                        spawn_pokemons(current_chunk)
                        create_trees(current_chunk, 0.75, self.max_height)
                        grow_grass(current_chunk, 0.6, self.max_height)
                        chunk_bar()

        if self.town_map:
            self.town_map_img = generate_town_map(self)

    def get_chunk(self, x: int, y: int) -> Optional[Chunk]:
        try:
            return self.chunks[y][x]
        except IndexError:
            return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size_h and 0 <= y < self.size_v

    def parse_to_coordinate_on_map(self, c: Chunk, x: int, y: int) -> tuple[int, int]:
        cx, cy = c.chunk_x, c.chunk_y
        x_parsed, y_parsed = cx * self.chunk_size + x, cy * self.chunk_size + y
        return x_parsed, y_parsed

    def parse_to_coordinate_in_chunk(self, x: int, y: int) -> tuple[Chunk, int, int]:
        cx, cy = x // self.chunk_size, y // self.chunk_size
        x_parsed, y_parsed = x % self.chunk_size, y % self.chunk_size
        return self.get_chunk(cx, cy), x_parsed, y_parsed

    def get_height_map_pos(self, x: int, y: int) -> int:
        try:
            return self.height_map[y][x]
        except IndexError:
            return 0

    def get_height(self, c: Chunk, x: int, y: int) -> int:
        x_parsed, y_parsed = self.parse_to_coordinate_on_map(c, x, y)
        if self.in_bounds(x_parsed, y_parsed):
            return self.get_height_map_pos(x_parsed, y_parsed)
        else:
            return 0

    def change_height(self, c: Chunk, x: int, y: int, val: int) -> None:
        x_parsed, y_parsed = self.parse_to_coordinate_on_map(c, x, y)
        self.height_map[y_parsed][x_parsed] += val
