from enum import Enum

from pkmnMap.Coordinate import Coordinate
from pkmnMap.Chunk import Chunk
from pkmnMap.tiles.Tile import Tile


def create_lakes_and_sea(self, sea_threshold=0.20) -> None:

    def validate(x0: int, y0: int) -> bool:
        return self.in_bounds(x0, y0) and self.get_height_map_pos(x0, y0) <= 0 and (x0, y0) not in current_water

    seen = set()
    water_queue = set()
    current_water = set()
    for y in range(self.size_v):
        for x in range(self.size_h):
            if (x, y) not in seen and self.height_map[y][x] < 0.5:
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
                    self.water_tiles.union(current_water)
                    if len(current_water) / (self.size_v * self.size_h) >= sea_threshold:
                        self.sea_tiles = self.sea_tiles.union(current_water)
                    else:
                        self.lake_tiles = self.lake_tiles.union(current_water)
                    current_water = set()


# Creates rivers for a Chunk
def create_rivers(self, chunk: Chunk, lake_tiles: set[tuple[int, int]], threshold, no_sprite=False):
    dark_water_height = -0.5
    for y in range(chunk.size):
        for x in range(chunk.size):
            h = chunk.get_height_exact(x, y)
            if round(h) <= 0:
                if no_sprite:
                    specific_tile = Tile("WATER", 0, 3 if h > dark_water_height else 6)
                else:
                    raw_pos = chunk.height_map_pos(x, y)
                    if raw_pos in lake_tiles:
                        water_type = 0
                    elif h > dark_water_height:
                        water_type = 1
                    else:
                        water_type = 2
                    curr_surrounding = get_surrounding_tiles(chunk, x, y, threshold)
                    tile = get_tile_from_surrounding(curr_surrounding)
                    specific_tile = WaterTiles.specific_tile(tile, water_type)
                chunk.set_tile("GROUND0", x, y, specific_tile)


def get_surrounding_tiles(chunk, x, y, threshold: int):
    return [[0 if chunk.get_height_exact(hx, hy) < threshold else 1 for hx in range(x - 1, x + 2)] for hy in range(y - 1, y + 2)]


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


# Creates sandy path around rivers; inside a simplex noise field
def create_beach(self, max_inland_size: int, threshold: int) -> set[tuple[int, int]]:
    def check_for_water_around(x0: int, y0: int, radius: int) -> bool:
        for check_y in range(y0 - radius, y0 + radius + 1):
            for check_x in range(x0 - radius, x0 + radius + 1):
                chunk0, cx0, cy0 = self.parse_to_coordinate_in_chunk(check_x, check_y)
                if chunk0 is not None and chunk0.get_height(cx0, cy0) == 0:
                    return True
        return False

    beach_tiles: set[tuple[int, int]] = set()
    new_beach_tiles: set[tuple[int, int]] = set()
    for y in range(self.size_v):
        for x in range(self.size_h):
            if round(self.get_height_map_pos(x, y)) == 1:
                chunk, cx, cy = self.parse_to_coordinate_in_chunk(x, y)
                if check_for_water_around(x, y, 1):
                    chunk["GROUND0"][(cx, cy)] = Tile("PATH", 0, 27)
                    self.path_tiles.add(Coordinate(x, y))
                    new_beach_tiles.update({(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)})

    for i in range(max_inland_size - 1):
        i_distance_beach_tiles: set[tuple[int, int]] = set()
        for x, y in new_beach_tiles.difference(beach_tiles):
            if round(self.get_height_map_pos(x, y)) == 1:
                chunk, cx, cy = self.parse_to_coordinate_in_chunk(x, y)
                if chunk["GROUND0"][(cx, cy)] is None and (i == 0 or chunk.get_height_exact(cx, cy) < 0.8):  # i == 0 to prevent buggy path tiles so beach inland depth will always be at least 2
                    chunk["GROUND0"][(cx, cy)] = Tile("PATH", 0, 9)
                    self.path_tiles.add(Coordinate(x, y))
                    i_distance_beach_tiles.update({(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)})
        beach_tiles.update(new_beach_tiles)
        new_beach_tiles = i_distance_beach_tiles

    return beach_tiles
