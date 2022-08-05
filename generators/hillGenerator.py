import random
from enum import Enum

from mapClasses.tile import Tile


def create_edges(chunk, hill_type=0):
    create_hill_edges(chunk, hill_type)


def remove_faulty_heights(chunk, force=False):
    smooth = False
    while not smooth:
        smooth = True
        for y in range(0, chunk.size):
            for x in range(0, chunk.size):
                curr_surrounding = get_surrounding_tiles(chunk, x, y)
                height_change = get_tile_from_surrounding(curr_surrounding, FaultyHillTiles)
                if height_change is not None:
                    chunk.change_height(x, y, height_change)
                    if force:
                        smooth = False


def create_hill_edges(chunk, hill_type):
    for y in range(chunk.size):
        for x in range(chunk.size):
            if chunk.get_height(x, y) > 1:
                curr_surrounding = get_surrounding_tiles(chunk, x, y)
                tile = get_tile_from_surrounding(curr_surrounding, HillTiles)
                if tile is not None:
                    specific_tile = HillTiles.specific_tile(tile, hill_type)
                    if specific_tile == Tile("HILLS", 4, 0):
                        if random.random() < 0.01:
                            specific_tile = Tile("HILLS", 0, 4)
                    chunk.set_tile("HILLS", x, y, specific_tile)


def get_surrounding_tiles(chunk, x, y):
    curr_h = chunk.get_height(x, y)
    return [[chunk.get_height(hx, hy) - curr_h for hx in range(x - 1, x + 2)] for hy in range(y - 1, y + 2)]


def get_tile_from_surrounding(surrounding, tile_enum):
    for tile in tile_enum:
        if equal_surrounding(tile.value[0], surrounding):
            return tile.value[1]


def equal_surrounding(template, arr):
    if arr is not None:
        for y in range(3):
            for x in range(3):
                if template[y][x] is not None and template[y][x] != arr[y][x]:
                    return False
    return True


class HillTiles(Enum):

    @staticmethod
    def specific_tile(tile, tile_type):
        return Tile(tile.type, tile.x + tile_type * 5, tile.y)

    A = [[None, None, None], [0, 0, None], [-1, 0, None]], Tile("HILLS", 0, 1)
    B = [[None, None, None], [None, 0, 0], [None, 0, -1]], Tile("HILLS", 0, 2)
    F = [[None, None, None], [0, 0, 0], [None, -1, None]], Tile("HILLS", 4, 0)
    C1 = [[-1, 0, None], [0, 0, None], [None, None, None]], Tile("HILLS", 3, 0)
    C2 = [[None, 0, -1], [None, 0, 0], [None, None, None]], Tile("HILLS", 3, 0)
    E = [[None, 0, None], [-1, 0, None], [None, 0, None]], Tile("HILLS", 1, 0)
    G = [[None, 0, None], [None, 0, -1], [None, 0, None]], Tile("HILLS", 2, 0)
    H = [[None, -1, None], [0, 0, 0], [None, None, None]], Tile("HILLS", 3, 0)
    I = [[None, -1, None], [-1, 0, 0], [None, 0, None]], Tile("HILLS", 1, 1)
    J = [[None, 0, None], [-1, 0, 0], [None, -1, None]], Tile("HILLS", 3, 1)
    K = [[None, 0, None], [0, 0, -1], [None, -1, None]], Tile("HILLS", 4, 1)
    L = [[None, -1, None], [0, 0, -1], [None, 0, None]], Tile("HILLS", 2, 1)


class FaultyHillTiles(Enum):

    X1 = [[None, -1, None], [None, 0, None], [None, -1, None]], -1
    X2 = [[None, 1, None], [None, 0, None], [None, 1, None]], 1
    X3 = [[None, None, None], [-1, 0, -1], [None, None, None]], -1
    X4 = [[None, None, None], [1, 0, 1], [None, None, None]], 1
