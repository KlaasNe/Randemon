from enum import Enum

from alive_progress import alive_bar

from mapClasses import Map
from mapClasses.chunk import Chunk
from mapClasses.tile import Tile


def create_lakes_and_sea(rmap: Map, sea_threshold=0.20) -> None:

    def validate(x0: int, y0: int) -> bool:
        return rmap.in_bounds(x0, y0) and rmap.get_height_parsed_pos(x0, y0) <= 0 and (x0, y0) not in current_water

    seen = set()
    water_queue = set()
    current_water = set()
    with alive_bar(rmap.size_v * rmap.size_h, title="Dividing into lakes and seas", theme="classic") as water_bar:
        for y in range(rmap.size_v):
            for x in range(rmap.size_h):
                if rmap.height_map[y][x] <= 0 and (x, y) not in seen:
                    new_water_found = True
                    water_queue.add((x, y))
                    while len(water_queue) > 0:
                        (x, y) = water_queue.pop()
                        current_water.add((x, y))
                        seen.add((x, y))

                        if validate(x + 1, y):
                            water_queue.add((x + 1, y))
                        if validate(x - 1, y):
                            water_queue.add((x - 1, y))
                        if validate(x, y + 1):
                            water_queue.add((x, y + 1))
                        if validate(x, y - 1):
                            water_queue.add((x, y - 1))
                    if new_water_found:
                        if len(current_water) / (rmap.size_v * rmap.size_h) >= sea_threshold:
                            rmap.sea_tiles = rmap.sea_tiles.union(current_water)
                        else:
                            rmap.lake_tiles = rmap.lake_tiles.union(current_water)
                        current_water = set()
                water_bar()


# Creates rivers for a chunk
def create_rivers(chunk: Chunk, lake_tiles: set[tuple[int, int]]):
    for y in range(chunk.size):
        for x in range(chunk.size):
            if chunk.get_height(x, y) <= 0:
                raw_pos = chunk.height_map_pos(x, y)
                water_type = 0 if raw_pos in lake_tiles else 1
                curr_surrounding = get_surrounding_tiles(chunk, x, y)
                tile = get_tile_from_surrounding(curr_surrounding)
                chunk.set_tile("GROUND0", x, y, WaterTiles.specific_tile(tile, water_type))


def get_surrounding_tiles(chunk, x, y):
    return [[max(0, chunk.get_height(hx, hy)) for hx in range(x - 1, x + 2)] for hy in range(y - 1, y + 2)]


def get_tile_from_surrounding(surrounding):
    for tile in WaterTiles:
        template = [[c for c in s] for s in tile.value[0].splitlines()]
        if equal_surrounding(template, surrounding):
            return tile.value[1]


def equal_surrounding(template, arr):
    if arr is not None:
        for y in range(3):
            for x in range(3):
                if template[y][x] != 'a' and template[y][x] != str(arr[y][x]):
                    return False
    return True


class WaterTiles(Enum):

    @staticmethod
    def specific_tile(tile, tile_type):
        return Tile(tile.type, tile.x, tile.y + tile_type * 3)

    O = "000\n000\n000", Tile("WATER", 0, 0)
    A = "100\n000\n000", Tile("WATER", 2, 2)
    B = "001\n000\n000", Tile("WATER", 1, 2)
    X1 = "000\n000\n001", Tile("WATER", 3, 2)
    X2 = "000\n000\n100", Tile("WATER", 4, 2)
    C = "a0a\n000\na0a", Tile("WATER", 0, 0)
    D = "a0a\na00\na0a", Tile("WATER", 1, 0)
    E = "a0a\n000\naaa", Tile("WATER", 4, 0)
    F = "a0a\n00a\na0a", Tile("WATER", 2, 0)
    G = "aaa\n000\na0a", Tile("WATER", 3, 0)
    H = "aaa\na00\na0a", Tile("WATER", 3, 1)
    I = "a0a\na00\naaa", Tile("WATER", 1, 1)
    J = "a0a\n00a\naaa", Tile("WATER", 2, 1)
    K = "aaa\n00a\na0a", Tile("WATER", 4, 1)
    default = "aaa\naaa\naaa", Tile("WATER", 0, 0)


# Creates sandy path around rivers; inside a perlin noise field
def create_beach(rmap: Map) -> None:
    def check_for_water_around(x0: int, y0: int, radius: int) -> bool:
        for check_y in range(y0 - radius, y0 + radius + 1):
            for check_x in range(x0 - radius, x0 + radius + 1):
                chunk0, cx0, cy0 = rmap.parse_to_chunk_coordinate(check_x, check_y)
                if chunk0 is not None and chunk0["GROUND0"].get_tile_type(cx0, cy0) == "WATER":
                    return True
        return False

    for y in range(rmap.size_v):
        for x in range(rmap.size_h):
            if rmap.get_height_parsed_pos(x, y) == 1:
                chunk, cx, cy = rmap.parse_to_chunk_coordinate(x, y)
                if chunk["GROUND0"][(cx, cy)] is None and check_for_water_around(x, y, 4):
                    chunk["GROUND0"][(cx, cy)] = Tile("PATH", 0, 9)
