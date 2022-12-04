from enum import Enum
from random import shuffle

from mapClasses import Map
from mapClasses.chunk import Chunk
from mapClasses.layer import Layer
from mapClasses.tile import Tile
from mapClasses.tile.TileWeights import TileWeights
from mapClasses.tile.WeightTile import WeightTile


def get_path_type(layer: Layer, x: int, y: int) -> int:
    tile = layer[(x, y)]
    return tile.y // 3 if type(tile) == Tile and tile.type == "PATH" else None


def create_path(rmap: Map, separated: bool = True) -> None:
    for y in range(rmap.size_v):
        for x in range(rmap.size_h):
            chunk, cx, cy = rmap.parse_to_chunk_coordinate(x, y)
            tile: Tile = chunk["GROUND0"][(cx, cy)]
            if tile is not None and tile.type == "PATH":
                path_type = tile.y // 3
                prev_surrounding = get_surrounding_tiles(rmap, x, y, path_type, separated)
                tile = get_tile_from_surrounding(prev_surrounding)
                if tile is None:
                    chunk["GROUND0"].remove_tile(cx, cy)
                else:
                    chunk["GROUND0"][(cx, cy)] = PathTiles.specific_tile(tile, path_type)


def get_surrounding_tiles(rmap: Map, x: int, y: int, path_type: int, separated: bool) -> list[list]:
    surrounding = []
    for py in range(y - 1, y + 2):
        row = []
        for px in range(x - 1, x + 2):
            chunk, cx, cy = rmap.parse_to_chunk_coordinate(px, py)
            if chunk is not None:
                pt = get_path_type(chunk["GROUND0"], cx, cy)
                valid = (pt == path_type or any([path_type == 3 and pt == 9, path_type == 9 and pt == 3])) if separated else pt is not None
                row.append(1 if valid or (path_type == 3 and chunk.get_height(cx, cy) == 0) else 0)
        surrounding.append(row)
    return surrounding


def get_tile_from_surrounding(surrounding) -> Tile:
    for tile in PathTiles:
        template = [[c for c in s] for s in tile.value[0].splitlines()]
        if equal_surrounding(template, surrounding):
            return tile.value[1]


def equal_surrounding(template, arr):
    if arr is not None:
        for y in range(3):
            for x in range(3):
                try:
                    if template[y][x] != 'a' and template[y][x] != str(arr[y][x]):
                        return False
                except IndexError:
                    return False
    return True


class PathTiles(Enum):

    @staticmethod
    def specific_tile(tile: Tile, tile_type: int) -> Tile:
        return Tile("PATH", tile.x, tile.y + tile_type * 3)

    A = "111\n111\n011", Tile("PATH", 2, 2)
    B = "111\n111\n110", Tile("PATH", 1, 2)
    C = "110\n111\n111", Tile("PATH", 3, 2)
    D = "011\n111\n111", Tile("PATH", 4, 2)
    E = "a1a\n111\na1a", Tile("PATH", 0, 0)
    F = "a1a\n0a1\na1a", Tile("PATH", 1, 0)
    G = "a1a\n1a1\na0a", Tile("PATH", 4, 0)
    H = "a1a\n1a0\na1a", Tile("PATH", 2, 0)
    I = "a0a\n1a1\na1a", Tile("PATH", 3, 0)
    J = "a0a\n0a1\na1a", Tile("PATH", 3, 1)
    K = "a1a\n0a1\na0a", Tile("PATH", 1, 1)
    L = "a1a\n1a0\na0a", Tile("PATH", 2, 1)
    M = "a0a\n1a0\na1a", Tile("PATH", 4, 1)
    # DEFAULT = "aaa\naaa\naaa", Tile("PATH", 0, 1)


def is_actual_path(layer, x, y):
    return get_path_type(layer, x, y) not in [None, 3, 9]


def place_path_tile(chunk: Chunk, x: int, y: int, path_type: int) -> None:
    if chunk.get_height(x, y) > 0:
        if chunk.get_tile("GROUND0", x, y) is None:
            chunk.set_tile("GROUND0", x, y, Tile("PATH", 0, path_type * 3))
    elif chunk.get_tile_type("GROUND0", x, y) == "WATER":
        chunk.set_tile("GROUND0", x, y, Tile("ROAD", -1, -1))


def draw_path2(chunk: Chunk, path_type: int):
    def init_weight_tiles():
        weights_array = []
        for wy in range(chunk.size):
            weights_row = []
            for wx in range(chunk.size):
                weights_row.append(WeightTile(wx, wy, determine_weight(chunk, wx, wy)))
            weights_array.append(weights_row)
        return weights_array

    def find_min_tile():
        try:
            return min([chunk_wght_tiles[y][x] for (x, y) in handle_tiles])
        except ValueError:
            return None

    def find_closest_connected_building(x, y):
        bd = None
        min_dist = 999999
        buildings_list = chunk.buildings
        for building in connected_buildings if len(connected_buildings) >= 2 else buildings_list:
            bx, by = building.get_abs_door_pos()
            if (bx, by) != (x, y):
                dist = abs(x - bx) + abs(y - by)
                if min_dist > dist:
                    min_dist = dist
                    bd = building
        return bd

    def handle_current_tile():
        cx, cy = curr_tile.x, curr_tile.y
        tx, ty = target_tile.x, target_tile.y
        for nx, ny in [(cx, cy - 1), (cx, cy + 1), (cx - 1, cy), (cx + 1, cy)]:
            if not chunk.out_of_bounds(nx, ny):
                ntile = chunk_wght_tiles[ny][nx]
                if not ntile.visited and not chunk.out_of_bounds(nx, ny) and ntile.weight < TileWeights.IMPASSABLE.value:
                    new_dist = curr_tile.dist + chunk_wght_tiles[cy][cx].weight + (abs(tx - cx) + abs(ty - cy))
                    if new_dist < ntile.dist:
                        ntile.prev = curr_tile
                        ntile.dist = new_dist
                        handle_tiles[(nx, ny)] = ntile
        curr_tile.visited = True
        handle_tiles.pop((cx, cy))

    def make_path_double(p):
        path_extention = set()
        for pos in p:
            for y in range(pos.y - 1, pos.y + 1):
                for x in range(pos.x - 1, pos.x + 1):
                    path_extention.add((x, y))

        for (x, y) in path_extention:
            place_path_tile(chunk, x, y, path_type)

    connected_buildings = set()
    chunk_wght_tiles = init_weight_tiles()
    shuffle(chunk.buildings)
    for b in chunk.buildings:
        connected_buildings.add(b)
        handle_tiles = {}
        start_x, start_y = b.get_abs_door_pos()
        curr_tile = chunk_wght_tiles[start_y][start_x]
        curr_tile.dist = 0
        handle_tiles[(curr_tile.x, curr_tile.y)] = curr_tile
        target = find_closest_connected_building(curr_tile.x, curr_tile.y)
        if target is None: break
        connected_buildings.add(target)
        end_x, end_y = target.get_abs_door_pos()
        target_tile = chunk_wght_tiles[end_y][end_x]
        while not len(handle_tiles) == 0 and curr_tile.dist < 999999:
            curr_tile = find_min_tile()
            if curr_tile is None: break
            handle_current_tile()
            if curr_tile == target_tile: break

        path = set()
        while curr_tile is not None:
            path.add(curr_tile)
            chunk_wght_tiles[curr_tile.y][curr_tile.x].weight = TileWeights.PATH.value
            curr_tile = curr_tile.prev
            try:
                if curr_tile == curr_tile.prev.prev: break
            except AttributeError:
                pass

        for y in range(chunk.size):
            for wght_tile in chunk_wght_tiles[y]:
                wght_tile.dist = 999999
                wght_tile.visited = False

        make_path_double(path)

    create_stairs(chunk, chunk.layers["GROUND0"], chunk.layers["GROUND1"])
    create_bridges(chunk, chunk.layers["GROUND0"])
    create_lanterns(chunk)


def determine_weight(chunk: Chunk, x, y, avoid_hill_corners=True):
    def is_2x2_tile_type(layer, x, y, tile_type):
        return any((chunk.get_tile_type(layer, x, y) == tile_type,
                   chunk.get_tile_type(layer, x - 1, y) == tile_type,
                   chunk.get_tile_type(layer, x, y - 1) == tile_type,
                    chunk.get_tile_type(layer, x - 1, y - 1) == tile_type))

    def is_corner(x, y):
        return chunk.has_tile_in_layer_at("HILLS", x, y) and chunk.get_tile("HILLS", x, y).y in [1, 3] or \
               chunk.get_tile("HILLS", x, y) == Tile("HILLS", 0, 2) or \
               chunk.get_tile("HILLS", x, y) == Tile("HILLS", 3, 0) and chunk.has_tile_in_layer_at("HILLS", x, y - 1)

    if is_2x2_tile_type("BUILDINGS", x, y, "BUILDINGS"): return TileWeights.IMPASSABLE.value
    if is_2x2_tile_type("FENCE", x, y, "FENCE"): return TileWeights.IMPASSABLE.value
    if avoid_hill_corners and any((is_corner(x, y), is_corner(x - 1, y), is_corner(x, y - 1), is_corner(x - 1, y - 1))): return TileWeights.IMPASSABLE.value
    if is_2x2_tile_type("HILLS", x, y, "HILLS"): return TileWeights.HILL.value
    if is_2x2_tile_type("GROUND0", x, y, "WATER"): return TileWeights.WATER.value
    if is_actual_path(chunk.layers["GROUND0"], x - 1, y - 1) and\
            is_actual_path(chunk.layers["GROUND0"], x - 1, y) and\
            is_actual_path(chunk.layers["GROUND0"], x, y - 1) and\
            is_actual_path(chunk.layers["GROUND0"], x, y):
        return TileWeights.PATH.value
    if is_2x2_tile_type("GROUND0", x, y, "PATH"): return TileWeights.GRASS.value
    return TileWeights.GRASS.value if is_2x2_tile_type("GROUND0", x, y, None) else TileWeights.IMPASSABLE.value


def create_bridges(chunk, layer):
    for y in range(chunk.size):
        for x in range(chunk.size):
            if layer[(x, y)] == Tile("ROAD", -1, -1):
                if layer.get_tile_type(x, y - 1) == "WATER":
                    layer[(x, y)] = Tile("ROAD", 0, 0)
                    layer[(x, y + 1)] = Tile("ROAD", 0, 1)
                elif layer.get_tile_type(x, y + 1) == "WATER":
                    layer[(x, y - 1)] = Tile("ROAD", 0, 0)
                    layer[(x, y)] = Tile("ROAD", 0, 1)
                elif layer.get_tile_type(x - 1, y) == "WATER":
                    layer[(x, y)] = Tile("ROAD", 1, 0)
                    layer[(x + 1, y)] = Tile("ROAD", 1, 1)
                elif layer.get_tile_type(x + 1, y, ) == "WATER":
                    layer[(x, y)] = Tile("ROAD", 1, 1)
                    layer[(x - 1, y)] = Tile("ROAD", 1, 0)
                else:
                    layer[(x, y)] = Tile("PATH", 0, 10)

            if layer.get_tile_type(x, y - 1) == "ROAD" and layer.get_tile_type(x, y) == "WATER":
                chunk.set_tile("GROUND1", x, y, Tile("DECO", 6, 0))


def create_stairs(chunk, pl, bl):

    def path_above(x, y):
        return is_actual_path(pl, x, y - 1)

    def path_under(x, y):
        return is_actual_path(pl, x, y + 1)

    def path_left(x, y):
        return is_actual_path(pl, x - 1, y)

    def path_right(x, y):
        return is_actual_path(pl, x + 1, y)

    for py in range(chunk.size):
        for px in range(chunk.size):
            if chunk.get_height(px, py) > 1 and pl.get_tile_type(px, py) == "PATH" and bl.get_tile_type(px, py) is None:
                if path_above(px, py) and path_under(px, py) and (path_left(px, py) or path_right(px, py)):
                    if chunk.get_height(px, py) > chunk.get_height(px, py - 1):
                        bl.set_tile(px, py, Tile("ROAD", 3, 0))
                        bl.set_tile(px + 1, py, Tile("ROAD", 3, 1))

                    elif chunk.get_height(px, py) > chunk.get_height(px, py + 1):
                        bl.set_tile(px, py, Tile("ROAD", 2, 0))
                        bl.set_tile(px + 1, py, Tile("ROAD", 2, 1))

                elif path_left(px, py) and path_right(px, py) and path_under(px, py):
                    if chunk.get_height(px, py) > chunk.get_height(px - 1, py):
                        bl.set_tile(px, py, Tile("ROAD", 4, 0))
                        bl.set_tile(px, py + 1, Tile("ROAD", 4, 1))

                    elif chunk.get_height(px, py) > chunk.get_height(px + 1, py):
                        bl.set_tile(px, py, Tile("ROAD", 5, 0))
                        bl.set_tile(px, py + 1, Tile("ROAD", 5, 1))


def create_lanterns(chunk: Chunk):
    from random import random

    def check_availability_zone(x1, y1, x2, y2):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if chunk.has_tile_in_layer_at("GROUND0", x, y) or chunk.has_tile_in_layer_at("HILLS", x, y) \
                        or chunk.has_tile_in_layer_at("BUILDINGS", x, y) or chunk.has_tile_in_layer_at("GROUND2", x, y):
                    return False
        return True

    for y in range(chunk.size):
        for x in range(chunk.size):
            if random() < 0.08:
                if chunk.get_tile_type("GROUND1", x, y) != "FENCES":
                    if is_actual_path(chunk["GROUND0"], x - 1, y) and not chunk.has_tile_in_layer_at("BUILDINGS", x - 1, y) and not chunk.has_tile_in_layer_at("GROUND2", x - 1, y):
                        if check_availability_zone(x, y - 2, x + 2, y + 1):
                            chunk.set_tile("GROUND2", x, y, Tile("DECO", 4, 2))
                            chunk.set_tile("GROUND2", x, y - 1, Tile("DECO", 4, 1))
                            chunk.set_tile("GROUND2", x, y - 2, Tile("DECO", 4, 0))
                            chunk.set_tile("GROUND2", x + 1, y, Tile("DECO", 5, 2))
                    if is_actual_path(chunk["GROUND0"], x + 1, y) and not chunk.has_tile_in_layer_at("BUILDINGS", x + 1, y) and not chunk.has_tile_in_layer_at("GROUND2", x + 1, y):
                        if check_availability_zone(x, y - 2, x, y + 1):
                            chunk.set_tile("GROUND2", x, y, Tile("DECO", 3, 2))
                            chunk.set_tile("GROUND2", x, y - 1, Tile("DECO", 3, 1))
                            chunk.set_tile("GROUND2", x, y - 2, Tile("DECO", 3, 0))


def remove_path(chunk: Chunk):
    delete_pos = set[tuple[int, int]]()

    for x, y in chunk["GROUND0"].get_ex_pos():
        if chunk.get_tile_type("GROUND0", x, y) == "PATH":
            delete_pos.add((x, y))

    for x, y in delete_pos:
        chunk.remove_tile("GROUND0", x, y)
