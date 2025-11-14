import json
from random import random

from PIL import Image
from colorama import Fore
from colorama import Style
from typing import Optional, Iterator

# TODO move all building business to chunks.. This should be chunk business
# TODO same for spawning pokemons, that's chunk business
from buildings.BuildingTheme import BuildingTheme
from buildings.BuildingTypes import BuildingThemes, BuildingTypes
from timeit import timeit
from ._pokemonGenerator import spawn_pokemons
# TODO move hill generator stuff to the heightmap business i guess?
from ._hillgenerator import *
from .HeightMap import HeightMap
from .Chunk import Chunk
from .PkmnMapInterface import PkmnMapInterface

from ._pathgenerator import remove_path  # TODO wth bruh clean this up!!!!!


class PkmnMap(PkmnMapInterface):
    from ._watergenerator import create_rivers, create_beach
    from ._minimapgenerator import generate_mini_map
    from ._buildinggenerator import spawn_building, spawn_functional_buildings
    from ._heightmapgenerator import draw_height_map, smooth_height
    from ._pathgenerator import draw_path2, create_path, create_route_path
    from ._plantgenerator import create_trees, grow_grass

    def __init__(self,
                 chunk_nb_h: int,
                 chunk_nb_v: int,
                 chunk_size: int,
                 seed: int,
                 max_buildings_per_chunk: int = 16,
                 island: bool = False,
                 make_height_map: bool = False,
                 themed_towns: bool = True,
                 terrain_chaos: int = 4,
                 max_height: int = 6) -> None:

        self.chunk_size: int = chunk_size
        self.chunk_nb_h: int = chunk_nb_h
        self.chunk_nb_v: int = chunk_nb_v
        self.size_h: int = self.chunk_size * self.chunk_nb_h
        self.size_v: int = self.chunk_size * self.chunk_nb_v
        self.max_buildings_per_chunk = max_buildings_per_chunk
        self.seed: int = seed
        self.draw_height_map = make_height_map
        self.themed_towns = themed_towns
        self.max_height = max_height
        random.seed(self.seed)
        print(Fore.LIGHTBLUE_EX + "seed = " + Fore.LIGHTYELLOW_EX + str(self.seed) + Style.RESET_ALL)
        print("Creating terrain...")
        self.off_x, self.off_y = random.randint(0, 10000000), random.randint(0, 10000000)
        self.height_map = HeightMap((self.chunk_nb_h, self.chunk_nb_v), self.chunk_size, self.off_x, self.off_y,
                                    self.max_height, 0.0, island).remove_faulty_heights()
        # self.height_map = generate_height_map_from_image("heightMaps/earthLandMassHeight.png")
        # self.smooth_height()

        self.chunks: list[list[Chunk]] = [
            [Chunk(self.height_map, chunk_size, x, y, self.off_x + x * self.chunk_size,
                   self.off_y + y * self.chunk_size, self.max_buildings_per_chunk) for x in
             range(chunk_nb_h)] for y in range(chunk_nb_v)]


        self.water_tiles: set[tuple[int, int]] = set()
        self.lake_tiles: set[tuple[int, int]] = set()
        self.sea_tiles: set[tuple[int, int]] = set()
        self.path_tiles: set[Coordinate] = set()
        self.beach_tiles: set[tuple[int, int]] = set()
        self.towns: set[Coordinate] = set()
        self.route_chunks: set[Coordinate] = set()
        self.town_map_img: Image = None

    def __iter__(self) -> Iterator[Chunk]:
        for chunk_row in self.chunks:
            for chunk in chunk_row:
                yield chunk

    @timeit
    def with_beaches(self, max_beach_inland_depth: int, water_threshold: int) -> "PkmnMap":
        # create_lakes_and_sea(self) TODO fix this (maybe ever)
        self.beach_tiles = self.create_beach(max_beach_inland_depth, water_threshold)

        return self

    @timeit
    def with_mini_map(self) -> "PkmnMap":
        self.generate_mini_map()

        return self

    @timeit
    def with_routes(self, looping_chance: float = 0) -> "PkmnMap":
        def is_connected(branches, start, end):
            nodes: set[Coordinate] = {start}
            seen: set[Coordinate] = set()
            while nodes:
                node = nodes.pop()
                if node == end:
                    return True

                for branch in branches:
                    add_node = None
                    if branch[0] == node:
                        add_node = branch[1]
                    elif branch[1] == node:
                        add_node = branch[0]

                    if add_node and add_node not in seen:
                        nodes.add(add_node)
                        seen.add(node)

            return False

        tree: set[tuple[Coordinate, Coordinate]] = set()
        edges = sorted([
            (town1, town2, town1.distance(town2))
            for town1 in self.towns
            for town2 in self.towns
            if town1 != town2
        ], key=lambda i: i[2])
        for edge in edges:
            if not is_connected(tree, edge[0], edge[1]):
                tree.add((edge[0], edge[1]))

        chunks_on_route: set[Coordinate] = set()
        for town1, town2 in tree:
            queue: list[tuple[Coordinate, int]] = [(town1, town1.distance(town2))]
            visited: set[Coordinate] = set()
            curr_pos = None
            previous: dict[str, Optional[Coordinate]] = {str(town1): None}
            while queue and curr_pos != town2:
                curr_pos, curr_dist = queue.pop()
                for pos in curr_pos.nesw():
                    if pos not in visited and pos.in_bounds((0, 0), (self.chunk_nb_h - 1, self.chunk_nb_v - 1)):
                        dist = pos.distance(town2)
                        if dist < curr_dist:
                            queue.append((pos, dist))
                            previous[str(pos)] = curr_pos
                        else:
                            visited.add(pos)
                        visited.add(curr_pos)

                sorted(queue, key=lambda i: i[1])

            route: list[Coordinate] = [town2]
            prev: Coordinate = town2
            while prev is not None:
                chunks_on_route.add(prev)
                prev = previous[str(prev)]
                route.append(prev)

        for chunk_coordinate in chunks_on_route:
            current_chunk = self.chunks[chunk_coordinate.y][chunk_coordinate.x]
            if chunk_coordinate.up() in chunks_on_route:
                current_chunk.route[0] = True  # North

            if chunk_coordinate.right() in chunks_on_route:
                current_chunk.route[1] = True  # East

            if chunk_coordinate.down() in chunks_on_route:
                current_chunk.route[2] = True  # South

            if chunk_coordinate.left() in chunks_on_route:
                current_chunk.route[3] = True  # West

        return self

    @timeit
    def with_buildings(self) -> "PkmnMap":
        for y in range(self.chunk_nb_v):
            for x in range(self.chunk_nb_h):
                current_chunk = self.chunks[y][x]
                self.try_place_buildings(current_chunk)

        return self

    @timeit
    def with_water(self) -> "PkmnMap":
        water_threshold = 2
        for y in range(self.chunk_nb_v):
            for x in range(self.chunk_nb_h):
                current_chunk = self.chunks[y][x]
                self.create_rivers(current_chunk, self.lake_tiles, water_threshold, no_sprite=True)

        return self

    @timeit
    def with_route_path(self) -> "PkmnMap":
        for y in range(self.chunk_nb_v):
            for x in range(self.chunk_nb_h):
                current_chunk = self.chunks[y][x]

                if not current_chunk.has_town and any(current_chunk.route):
                    self.create_route_path(current_chunk) # yo this kinda ugly idk man

        self.create_path()

        return self

    @timeit
    def create(self):
        # create_dirt_patches(self, self.off_x, self.off_y)

        for y in range(self.chunk_nb_v):
            for x in range(self.chunk_nb_h):
                current_chunk = self.chunks[y][x]
                spawn_pokemons(current_chunk)
                self.create_trees(current_chunk, 0.75, self.max_height)
                self.grow_grass(current_chunk, 0.6, self.max_height)

    def try_place_buildings(self, chunk: Chunk) -> "PkmnMap":
        powerplant = True
        create_edges(chunk, hill_type=0)
        # create_rivers(current_chunk, self.lake_tiles)
        if self.max_buildings_per_chunk > 0 and chunk.chunk_x % 2 == 0 and chunk.chunk_y % 2 == 0:
            path_type = random.randint(0, 7)  # HELL YEAH MAGIC NUMBER
            if random.randint(0, 9) < 9:  # HELL YEAH magic number
                chunk.has_town = True
                valid_town = self.spawn_functional_buildings(chunk, path_type)
                if valid_town:
                    self.towns.add(Coordinate(chunk.chunk_x, chunk.chunk_y))
                    if self.themed_towns:
                        building_theme: BuildingTheme = BuildingThemes.get_random_theme().value
                    for b in range(random.randint(1, self.max_buildings_per_chunk)):
                        if self.themed_towns:
                            self.spawn_building(chunk,
                                                building_theme.get_random_building_type().value, path_type)
                        else:
                            self.spawn_building(chunk,
                                                BuildingTypes["H" + str(random.randint(0, 21))].value,
                                                path_type)
                    self.draw_path2(chunk, path_type)
                else:
                    chunk.has_town = False
                    chunk.clear_layer("BUILDINGS")
                    remove_path(chunk)
            else:
                if not powerplant:
                    self.spawn_building(chunk, BuildingTypes.POWERPLANT.value, path_type)

        return self

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

    def to_json(self) -> str:
        return json.dumps({
            "dimensions": {"x": self.chunk_nb_h, "y": self.chunk_nb_v},
            "Chunk": [[chunk.to_json() for chunk in chunk_row] for chunk_row in self.chunks]
        })
