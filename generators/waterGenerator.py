from enum import Enum

from noise import snoise2

from mapClasses import Tile


# Creates rivers for a chunk
def create_rivers(chunk):
    for y in range(chunk.size):
        prev_surrounding = None
        for x in range(chunk.size):
            if chunk.height_map[y][x] == 0:
                prev_surrounding = get_surrounding_tiles(chunk, x, y, prev_surrounding)
                chunk.set_tile("GROUND0", x, y, get_tile_from_surrounding(prev_surrounding))
            else:
                prev_surrounding = None


def get_surrounding_tiles(chunk, x, y, prev):
    if prev is None:
        return [[chunk.get_height(hx, hy, 0) for hx in range(x - 1, x + 2)] for hy in range(y - 1, y + 2)]
    else:
        new = [r[1:] for r in prev]
        for hy in range(3):
            new[hy].append(chunk.get_height(x + 1, y - 1 + hy, 0))
        return new


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
    A = "100\n000\n000", Tile("WATER", 2, 2)
    B = "001\n000\n000", Tile("WATER", 1, 2)
    C = "a0a\n000\na0a", Tile("WATER", 0, 0)
    D = "a0a\naa0\na0a", Tile("WATER", 1, 0)
    E = "a0a\n0a0\naaa", Tile("WATER", 4, 0)
    F = "a0a\n0aa\na0a", Tile("WATER", 2, 0)
    G = "aaa\n0a0\na0a", Tile("WATER", 3, 0)
    H = "aaa\naa0\na0a", Tile("WATER", 3, 1)
    I = "a0a\naa0\naaa", Tile("WATER", 1, 1)
    J = "a0a\n0aa\naaa", Tile("WATER", 2, 1)
    K = "aaa\n0aa\na0a", Tile("WATER", 4, 1)
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
