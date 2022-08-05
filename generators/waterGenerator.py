from enum import Enum

from alive_progress import alive_bar

from mapClasses.tile import Tile
from generators.heightMapGenerator import get_height


def create_lakes_and_sea(rmap, sea_threshold=0.20):

    def validate(x, y):
        return rmap.in_bounds(x, y) and rmap.get_height_raw_pos(x, y) <= 0 and (x, y) not in current_water

    seen = set()
    water_queue = set()
    current_water = set()
    new_water_found = False
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
def create_rivers(chunk):
    for y in range(chunk.size):
        for x in range(chunk.size):
            if chunk.get_height(x, y) <= 0:
                raw_pos = chunk.size * chunk.chunk_x + x, chunk.size * chunk.chunk_y + y
                water_type = 0 if raw_pos in chunk.map.lake_tiles else 1
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
        return Tile(tile.reader_name, tile.x, tile.y + tile_type * 3)

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
# def create_beach(layer, height_map, x_offset, y_offset):
#     def check_for_water_around(x, y, beach_width):
#         for around in range(0, (beach_width + 2) ** 2):
#             check_x = x + around % (beach_width + 2) - beach_width
#             check_y = y + around // (beach_width + 2) - beach_width
#             if layer.get_tile_type((check_x, check_y)) == "wa":
#                 return True
#         return False
#
#     octaves = 1
#     freq = 100
#     for y in range(0, layer.sy):
#         for x in range(0, layer.sx):
#             beach = snoise2((x + x_offset) / freq, (y + y_offset) / freq, octaves) + 0.5 > 0.5
#             if beach and ((x, y) not in layer.get_ex_pos()
#                           and height_map.get((x, y), 0) == 1
#                           and check_for_water_around(x, y, 4)):
#                 layer.set_tile((x, y), ("pa", 0, 9))
