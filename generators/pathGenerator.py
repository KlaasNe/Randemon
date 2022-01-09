from enum import Enum
from random import shuffle
from sys import maxsize

from mapClasses.tile import Tile
from mapClasses.tile.TileWeights import TileWeights
from mapClasses.tile.WeightTile import WeightTile


def get_path_type(layer, x, y):
    tile = layer.get_tile(x, y)
    return tile.y // 3 if tile is not None and tile.get_type() == "PATH" else None


def create_path(chunk):
    for y in range(chunk.size):
        prev_surrounding = None
        for x in range(chunk.size):
            if chunk.get_tile_type("GROUND0", x, y) == "PATH":
                prev_surrounding = get_surrounding_tiles(chunk, x, y, prev_surrounding)
                chunk.set_tile("GROUND0", x, y, PathTiles.specific_tile(get_tile_from_surrounding(prev_surrounding), 0))
            else:
                prev_surrounding = None


def get_surrounding_tiles(chunk, x, y, prev):
    if prev is None:
        return [[1 if chunk.get_tile_type("GROUND0", hx, hy) == "PATH" else 0 for hx in range(x - 1, x + 2)] for hy in range(y - 1, y + 2)]
    else:
        new = [r[1:] for r in prev]
        for hy in range(3):
            new[hy].append(1 if chunk.get_tile_type("GROUND0", x + 1, y - 1 + hy) == "PATH" else 0)
        return new


def get_tile_from_surrounding(surrounding):
    for tile in PathTiles:
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


class PathTiles(Enum):

    @staticmethod
    def specific_tile(tile, tile_type):
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
    default = "aaa\naaa\naaa", Tile("PATH", 0, 1)


def is_actual_path(layer, x, y):
    return get_path_type(layer, x, y) not in [None, 3]


def draw_path2(chunk, path_type):
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
        for nx, ny in [(cx, cy + 1), (cx, cy - 1), (cx + 1, cy), (cx - 1, cy)]:
            if not chunk.out_of_bounds(nx, ny):
                ntile = chunk_wght_tiles[ny][nx]
                if not ntile.visited and not chunk.out_of_bounds(nx, ny) and ntile.weight < TileWeights.IMPASSABLE.value:
                    new_dist = curr_tile.dist + chunk_wght_tiles[cy][cx].weight + (abs(tx - cx) + abs(ty - cy)) // 8
                    if new_dist < ntile.dist:
                        ntile.prev = curr_tile
                        ntile.dist = new_dist
                        handle_tiles[(nx, ny)] = ntile
        curr_tile.visited = True
        handle_tiles.pop((cx, cy))

    def make_path_double(p, path_type):
        path_extention = set()
        for pos in p:
            path_extention.add((pos.x, pos.y))
            path_extention.add((pos.x, pos.y - 1))
            path_extention.add((pos.x - 1, pos.y))
            path_extention.add((pos.x - 1, pos.y - 1))

        for (x, y) in path_extention:
            if chunk.height_map[y][x] >= 0:
                if chunk.get_tile("GROUND0", x, y) is None:
                    chunk.set_tile("GROUND0", x, y, Tile("PATH", 0, 0))
            # elif "pa" != pmap.ground.get_tile_type((x, y)):
            #     pmap.ground.set_tile((x, y), path_type)

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

        make_path_double(path, 0)

    # create_stairs(layer)
    # create_bridges(layer)


def determine_weight(chunk, x, y, avoid_hill_corners=True):
    def is_2x2_tile_type(layer, x, y, tile_type):
        return any((chunk.get_tile_type(layer, x, y) == tile_type,
                   chunk.get_tile_type(layer, x - 1, y) == tile_type,
                   chunk.get_tile_type(layer, x, y - 1) == tile_type,
                    chunk.get_tile_type(layer, x - 1, y - 1) == tile_type))

    def is_corner(x, y):
        return (x, y) in chunk.get_ex_pos("HILLS") and chunk.get_tile("HILLS", x, y).y in [1, 3] or \
               chunk.get_tile("HILLS", x, y) == Tile("HILLS", 3, 0) and (x, y - 1) in chunk.get_ex_pos("HILLS")

    if is_2x2_tile_type("BUILDINGS", x, y, "BUILDINGS"): return TileWeights.IMPASSABLE.value
    # if (x, y) in chunk.get_ex_pos("FENCE") or (x - 1, y) in chunk.get_ex_pos("FENCE") or (x, y - 1) in chunk.get_ex_pos("FENCE"): return TileWeights.IMPASSABLE
    # if chunk.ground.get_tile_type((x, y)) == "ro": return PATH_WEIGHT
    # if chunk.ground.get_tile_type((x, y - 1)) == "ro": return 999999
    # if chunk.ground.get_tile_type((x - 1, y)) == "ro": return 999999
    if avoid_hill_corners and any((is_corner(x, y), is_corner(x - 1, y), is_corner(x, y - 1), is_corner(x - 1, y - 1))): return TileWeights.IMPASSABLE.value
    if is_2x2_tile_type("HILLS", x, y, "HILLS"): return TileWeights.HILL.value
    if is_2x2_tile_type("GROUND0", x, y, "WATER"): return TileWeights.WATER.value
    if is_actual_path(chunk.layers["GROUND0"], x - 1, y - 1) and\
            is_actual_path(chunk.layers["GROUND0"], x - 1, y) and\
            is_actual_path(chunk.layers["GROUND0"], x, y - 1) and\
            is_actual_path(chunk.layers["GROUND0"], x, y):
        return TileWeights.PATH.value
    return TileWeights.GRASS.value if is_2x2_tile_type("GROUND0", x, y, None) else TileWeights.IMPASSABLE.value


# def draw_path(pmap, layer, house_path_type):
#     def initialize_dijkstra():
#         for y in range(pmap.height):
#             current_weight.append(pmap.width * [maxsize])
#             weight.append(weight_array[y])
#             visited.append(pmap.width * [False])
#             previous_tile.append(pmap.width * [(0, 0)])
#
#     def handle_current_tile():
#         curr_x = current_tile[0]
#         curr_y = current_tile[1]
#         visited[curr_y][curr_x] = True
#         for around_x, around_y in [(curr_x, curr_y - 1), (curr_x, curr_y + 1), (curr_x - 1, curr_y), (curr_x + 1, curr_y)]:
#             if not pmap.ground.out_of_bounds(around_x, around_y):
#                 new_weight = current_weight[curr_y][curr_x] + weight[around_y][around_x] + abs(target_tile[0] - curr_x) + abs(target_tile[1] - curr_y)
#                 if not visited[around_y][around_x] and current_weight[around_y][around_x] > new_weight:
#                     current_weight[around_y][around_x] = new_weight
#                     previous_tile[around_y][around_x] = current_tile
#                     handle_tiles[(around_x, around_y)] = new_weight
#         handle_tiles.pop(current_tile)
#
#     def find_closest_house(x, y):
#         closest_distance = 999999
#         closest_house = (x, y)
#         for house in already_connected:
#             if house != (x, y):
#                 if abs(house[0] - x) + abs(house[1] - y) < closest_distance:
#                     closest_distance = abs(house[0] - x) + abs(house[1] - y)
#                     closest_house = house
#         return closest_house
#
#     weight_array = {}
#     for y in range(pmap.height):
#         weight_array_row = []
#         for x in range(pmap.width):
#             weight_array_row.append(determine_weight(pmap, x, y))
#         weight_array[y] = weight_array_row
#
#     already_connected = set()
#     for front_door in range(len(pmap.front_doors)):
#         current_tile = pmap.front_doors[front_door]
#         if pmap.tile_heights.get(current_tile, -1) > pmap.highest_path:
#             pmap.highest_path = pmap.tile_heights[current_tile]
#         already_connected.add(current_tile)
#         if not current_tile: print("broken")
#         target_tile = find_closest_house(current_tile[0], current_tile[1])
#         already_connected.add(target_tile)
#         weight = []
#         current_weight = []
#         visited = []
#         previous_tile = []
#         handle_tiles = {}
#         initialize_dijkstra()
#
#         visited[current_tile[1]][current_tile[0]] = True
#         current_weight[current_tile[1]][current_tile[0]] = 0
#         previous_tile[current_tile[1]][current_tile[0]] = (0, 0)
#         handle_tiles[(current_tile[0], current_tile[1])] = 0
#         handle_current_tile()
#         while not current_tile == target_tile and current_weight[current_tile[1]][current_tile[0]] < 999999:
#             current_tile = find_min_tile()
#             handle_current_tile()
#
#         if current_weight[current_tile[1]][current_tile[0]] < 999999:
#             path = set()
#             while not previous_tile[current_tile[1]][current_tile[0]] == (0, 0):
#                 path.add(current_tile)
#                 if "pa" != layer.get_tile_type((current_tile[0], current_tile[1])):
#                     weight_array[current_tile[1]][current_tile[0]] = TileWeights.PATH
#                 current_tile = previous_tile[current_tile[1]][current_tile[0]]
#             path.add(current_tile)
#
#             make_path_double(pmap, path, house_path_type)
#
#     create_stairs(pmap, layer)
#     create_bridges(pmap, layer)


def create_bridges(pmap, layer):
    for y in range(pmap.height):
        for x in range(pmap.width):
            if layer.get_tile((x, y)) == ("ro", 0, 0):
                if layer.get_tile_type((x, y - 1)) == "wa":
                    layer.set_tile((x, y), ("ro", 0, 0))
                    layer.set_tile((x, y + 1), ("ro", 0, 1))
                elif layer.get_tile_type((x, y + 1)) == "wa":
                    layer.set_tile((x, y - 1), ("ro", 0, 0))
                    layer.set_tile((x, y), ("ro", 0, 1))
                elif layer.get_tile_type((x - 1, y)) == "wa":
                    layer.set_tile((x, y), ("ro", 1, 0))
                    layer.set_tile((x + 1, y), ("ro", 1, 1))
                elif layer.get_tile_type((x + 1, y), ) == "wa":
                    layer.set_tile((x, y), ("ro", 1, 1))
                    layer.set_tile((x - 1, y), ("ro", 1, 0))
                else:
                    layer.set_tile((x, y), ("pa", 0, 10))

            if "ro" == layer.get_tile_type((x, y - 1)) and "wa" == layer.get_tile_type((x, y)):
                pmap.decoration.set_tile((x, y), ("de", 6, 0))


def create_stairs(pmap, layer):

    def path_above(x, y):
        return is_actual_path(layer, x, y - 1)

    def path_under(x, y):
        return is_actual_path(layer, x, y + 1)

    def path_left(x, y):
        return is_actual_path(layer, x - 1, y)

    def path_right(x, y):
        return is_actual_path(layer, x + 1, y)

    for path_y in range(pmap.height):
        for path_x in range(pmap.width):
            if "pa" == layer.get_tile_type((path_x, path_y)) and pmap.tile_heights[(path_x, path_y)] > 1:
                if path_above(path_x, path_y) and path_under(path_x, path_y) and (path_left(path_x, path_y) or path_right(path_x, path_y)):
                    if pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x, path_y - 1), 0):
                        layer.set_tile((path_x, path_y), ("ro", 3, 0))
                        layer.set_tile((path_x + 1, path_y), ("ro", 3, 1))

                    elif pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x, path_y + 1), 0):
                        layer.set_tile((path_x, path_y), ("ro", 2, 0))
                        layer.set_tile((path_x + 1, path_y), ("ro", 2, 1))

                elif path_left(path_x, path_y) and path_right(path_x, path_y) and path_under(path_x, path_y):
                    if pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x - 1, path_y), 0):
                        layer.set_tile((path_x, path_y), ("ro", 4, 0))
                        layer.set_tile((path_x, path_y + 1), ("ro", 4, 1))

                    elif pmap.tile_heights.get((path_x, path_y), 0) > pmap.tile_heights.get((path_x + 1, path_y), 0):
                        layer.set_tile((path_x, path_y), ("ro", 5, 0))
                        layer.set_tile((path_x, path_y + 1), ("ro", 5, 1))


def create_lanterns(pmap):
    from random import random

    def check_availability_zone(x1, y1, x2, y2):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if (x, y) in pmap.ground.get_ex_pos() or (x, y) in pmap.buildings.get_ex_pos() or (x, y) in pmap.decoration.get_ex_pos():
                    return False
        return True

    for y in range(0, pmap.height):
        for x in range(0, pmap.width):
            if pmap.ground2.get_tile_type((x, y)) != "fe":
                if is_actual_path(pmap.ground, x - 1, y) and (x - 1, y) not in pmap.buildings.get_ex_pos() and (x - 1, y) not in pmap.ground2.get_ex_pos():
                    if random() < 0.08 and check_availability_zone(x, y - 2, x + 2, y + 1):
                        pmap.ground2.set_tile((x, y), ("de", 4, 2))
                        pmap.decoration.set_tile((x, y - 1), ("de", 4, 1))
                        pmap.decoration.set_tile((x, y - 2), ("de", 4, 0))
                        pmap.ground2.set_tile((x + 1, y), ("de", 5, 2))
                if is_actual_path(pmap.ground, x + 1, y) and (x + 1, y) not in pmap.buildings.get_ex_pos() and (x + 1, y) not in pmap.ground2.get_ex_pos():
                    if random() < 0.08 and check_availability_zone(x, y - 2, x, y + 1):
                        pmap.ground2.set_tile((x, y), ("de", 3, 2))
                        pmap.decoration.set_tile((x, y - 1), ("de", 3, 1))
                        pmap.decoration.set_tile((x, y - 2), ("de", 3, 0))
