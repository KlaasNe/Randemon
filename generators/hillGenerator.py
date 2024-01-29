import random
import re
from enum import Enum

from mapClasses.Coordinate import Coordinate
from mapClasses.chunk import Chunk
from mapClasses.tile import Tile


def create_edges(chunk, hill_type=0):
    create_hill_edges(chunk, hill_type)


def remove_faulty_heights(height_map, force=False):
    smooth = False
    warning_set = set()
    ignored_set = set()
    while not smooth:
        smooth = True
        for y in range(len(height_map)):
            for x in range(len(height_map[y])):
                curr_surrounding = get_surrounding_tiles_map(height_map, x, y)
                height_change = get_tile_from_surrounding(curr_surrounding, FaultyHillTiles)
                if height_change is not None and (x, y) not in ignored_set:
                    height_map[y][x] += height_change
                    if (x, y) in warning_set:
                        ignored_set.add((x, y))
                    else:
                        warning_set.add((x, y))

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
                    chunk.hill_tiles.add((x, y))


def get_surrounding_tiles(chunk: Chunk, x, y):
    c = Coordinate(x, y)
    curr_h = round(chunk.get_height(x, y))
    surr_str = ""
    if curr_h > 0:
        heights = []
        for hx, hy in c.around():
            heights.append(round(chunk.get_height(hx, hy)))
        surr_str = ''.join(
            "0" if surr_h == curr_h else ("l" if surr_h < curr_h else "h") for surr_h in heights
        )
    else:
        surr_str = "000000000"
    return surr_str


def get_surrounding_tiles_map(height_map, x, y):
    c = Coordinate(x, y)
    curr_h = round(height_map[y][x])
    surr_str = ""
    if curr_h >= 0:
        heights = []
        for hx, hy in c.around():
            heights.append(round(height_map[hy][hx]))
        surr_str = ''.join(
            "0" if surr_h == curr_h else ("l" if surr_h < curr_h else "h") for surr_h in heights
        )
    else:
        surr_str = "000000000"
    return surr_str


def get_tile_from_surrounding(surrounding, tile_enum):
    for tile in tile_enum:
        if equal_surrounding(tile.value[0], surrounding):
            return tile.value[1]


def equal_surrounding(template, arr):
    return re.findall(template, arr)


class HillTiles(Enum):

    @staticmethod
    def specific_tile(tile, tile_type):
        return Tile(tile.type, tile.x + tile_type * 5, tile.y)

    # A = [[None, None, None], [0, 0, None], [-1, 0, None]], Tile("HILLS", 0, 1)
    # B = [[None, None, None], [None, 0, 0], [None, 0, -1]], Tile("HILLS", 0, 2)
    # F = [[None, None, None], [0, 0, 0], [None, -1, None]], Tile("HILLS", 4, 0)
    # C1 = [[-1, 0, None], [0, 0, None], [None, None, None]], Tile("HILLS", 3, 0)
    # C2 = [[None, 0, -1], [None, 0, 0], [None, None, None]], Tile("HILLS", 3, 0)
    # E = [[None, 0, None], [-1, 0, None], [None, 0, None]], Tile("HILLS", 1, 0)
    # G = [[None, 0, None], [None, 0, -1], [None, 0, None]], Tile("HILLS", 2, 0)
    # H = [[None, -1, None], [0, 0, 0], [None, None, None]], Tile("HILLS", 3, 0)
    # I = [[None, -1, None], [-1, 0, 0], [None, 0, None]], Tile("HILLS", 1, 1)
    # J = [[None, 0, None], [-1, 0, 0], [None, -1, None]], Tile("HILLS", 3, 1)
    # K = [[None, 0, None], [0, 0, -1], [None, -1, None]], Tile("HILLS", 4, 1)
    # L = [[None, -1, None], [0, 0, -1], [None, 0, None]], Tile("HILLS", 2, 1)

    NA = "^0{9}$", None
    INSIDE_CORNER_LEFT_DOWN = "^.{3}00.l0.$", Tile("HILLS", 0, 1)
    INSIDE_CORNER_RIGHT_DOWN = "^.{4}00.0l$", Tile("HILLS", 0, 2)
    STRAIGHT_HORIZONTAL_FRONT = "^.{3}0{3}.l.$", Tile("HILLS", 4, 0)
    INSIDE_CORNER_LEFT_UP = "^l0.00.{4}$", Tile("HILLS", 3, 0)
    INSIDE_CORNER_RIGHT_UP = "^.0l.00.{3}$", Tile("HILLS", 3, 0)
    STRAIGHT_VERTICAL_LEFT = "^.0.l0..0.$", Tile("HILLS", 1, 0)
    STRAIGHT_VERTICAL_RIGHT = "^.0..0l.0.$", Tile("HILLS", 2, 0)
    STRAIGHT_HORIZONTAL_BACK = "^.l.0{3}.{3}$", Tile("HILLS", 3, 0)
    CORNER_LEFT_UP = "^.l.l00.0.$", Tile("HILLS", 1, 1)
    CORNER_LEFT_DOWN = "^.0.l00.l.$", Tile("HILLS", 3, 1)
    CORNER_RIGHT_DOWN = "^.0.00l.l.$", Tile("HILLS", 4, 1)
    CORNER_RIGHT_UP = "^.l.00l.0.$", Tile("HILLS", 2, 1)


class FaultyHillTiles(Enum):
    # X1 = [[None, -1, None], [None, 0, None], [None, -1, None]], -1
    # X2 = [[None, 1, None], [None, 0, None], [None, 1, None]], 1
    # X3 = [[None, None, None], [-1, 0, -1], [None, None, None]], -1
    # X4 = [[None, None, None], [1, 0, 1], [None, None, None]], 1
    X1 = "^.l..0..l.$", -1
    X2 = "^.h..0..h.$", 1
    X3 = "^...l0l...$", -1
    X4 = "^...h0h...$", 1
