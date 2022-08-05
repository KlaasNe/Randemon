import random
from math import sqrt

# Spawns a house on the map with house_front_path_type as its front porch
# Houses are spawned by chosing a random x and y coordinate, checking whether enough space is available for the given
# house if not, choose a new position. There's an upper limit to try find a building spot.
from buildings.Building import Building
from buildings.BuildingTypes import BuildingTypes
from mapClasses.chunk import Chunk
from mapClasses.tile import Tile


def spawn_building(chunk, building, fence_opt=True, mail_box_opt=True):
    # checks if a chosen position has enough free space for the house + spacing, starting from the top left corner
    def is_available_spot(x1, y1, x2, y2):
        if chunk.out_of_bounds(x1, y1) or chunk.out_of_bounds(x2, y2):
            return False
        for y in range(y1, y2 + 1):
            for x in range(x1 - 2, x2 + 1 + 2):
                if chunk.has_tile_at_layer("GROUND0", x, y) or chunk.has_tile_at_layer("FENCE", x, y):
                    return False
                if x1 <= x < x2 + 2 and y1 <= y < y2 + 1:
                    if chunk.has_tile_at_layer("BUILDINGS", x, y) or chunk.has_tile_at_layer("HILLS", x, y):
                        return False
        return True

    # Chooses a random x and y coordinate to try build a house
    # If a house already exists on the chosen coordinate, searches for the lower right corner of given house and when
    # enough space available, builds the house adjacent on the right to the house previously found
    def search_available_spot(building, cluster_radius, max_attempts):

        def get_random_coo():
            return random.randint(2, chunk.size - size_x), random.randint(2, chunk.size - size_y - 2)

        attempts = 1
        size_x, size_y = building.size
        try_x, try_y = get_random_coo()
        available = is_available_spot(try_x, try_y - 1, try_x + size_x, try_y + size_y + 2)
        while attempts < max_attempts and (
                not available or not is_inside_cluster(chunk, try_x, try_y, cluster_radius, 2)):
            attempts += 1
            try_x, try_y = get_random_coo()
            available = is_available_spot(try_x, try_y - 1, try_x + size_x, try_y + size_y + 2)
        return (try_x, try_y) if attempts <= max_attempts and available and is_inside_cluster(chunk, try_x, try_y, cluster_radius, 2) else False

    # search for the lower right corner of a house
    # def find_lower_right_of_house(x, y, size_y):
    #     while (x, y) in chunk.get_layer("BUILDINGS").get_ex_pos():
    #         if chunk.get_tile("BUILDINGS", x - 1, y).get_type() == "BUILDINGS": y += 1
    #         if chunk.get_tile("BUILDINGS", x, y - 1).get_type() == "BUILDINGS": x += 1
    #     return x, y - size_y

    size_x, size_y = building.size
    map_size_factor = max(chunk.size * chunk.size // 2500, 1) ** 2
    max_attempts = size_x * size_y * 100 * map_size_factor
    build_spot = search_available_spot(building, 25, max_attempts)
    if build_spot:
        build_building(chunk, building, build_spot, fence_opt, mail_box_opt)
        return True
    else:
        return False


def build_building(chunk: Chunk, building, build_spot, fence_opt=True, mail_box_opt=True):
    size_x, size_y = building.size
    house_x, house_y = build_spot
    for house_build_y in range(size_y):
        for house_build_x in range(size_x):
            chunk.set_tile("BUILDINGS", house_x + house_build_x, house_y + house_build_y,
                           Tile("BUILDINGS", building.t_pos[0] + house_build_x, building.t_pos[1] + house_build_y))
    chunk.buildings.append(Building(building, build_spot[0], build_spot[1]))
    for front_y in range(2):
        for front_x in range(size_x):
            chunk.set_tile("GROUND0", house_x + front_x, house_y + size_y + front_y, Tile("PATH", 0, 0))
    if mail_box_opt:
        if random.randint(0, 1) == 1 and \
                not chunk.has_tile_at_layer("BUILDINGS", house_x - 1, house_y + size_y - 2) and \
                not chunk.has_tile_at_layer("HILLS", house_x - 1, house_y + size_y - 2):
            chunk.set_tile("GROUND2", house_x - 1, house_y + size_y - 2, Tile("DECO", 7, 2))
            chunk.set_tile("GROUND2", house_x - 1, house_y + size_y - 1, Tile("DECO", 7, 3))

    if fence_opt and random.randint(1, 4) == 1:
        create_fence(chunk, house_x + size_x - 1, house_y + 1, 5, random.randint(0, 3), True)


# Checks whether a coordinate is at least in radius [distance] of [connections] houses
def is_inside_cluster(chunk, x, y, radius, connections):
    if len(chunk.buildings) == 0:
        return True

    found_connections = 0
    for building in chunk.buildings:
        front_door_x, front_door_y = building.get_pos()
        if sqrt((x - front_door_x) ** 2 + (y - front_door_y) ** 2) < radius:
            found_connections += 1
        if connections > len(chunk.buildings):
            if found_connections == len(chunk.buildings) - 1:
                return True
        else:
            if found_connections == connections:
                return True
    return False


def spawn_functional_buildings(chunk):
    pc = spawn_building(chunk, BuildingTypes.POKECENTER.value, fence_opt=False, mail_box_opt=False)
    g = spawn_building(chunk, BuildingTypes.GYM.value, fence_opt=False, mail_box_opt=False)
    pm = spawn_building(chunk, BuildingTypes.POKEMART.value, fence_opt=False, mail_box_opt=False)
    return pc and g and pm


# def is_special_building(pmap, x, y):
#     return isinstance(get_house_type(pmap, x, y), str)


# gives people a backyard surrounded by a fence
def create_fence(chunk, x, y, max_y, rel_fence_type, tree=False):
    def can_have_fence():
        curr_size = min(size_x // 2 + 1, max_y)
        new_max_y = curr_size
        for test_y in range(y - curr_size - 1, y):
            for test_x in range(x - size_x, x):
                if chunk.get_tile("GROUND0", test_x, test_y) == Tile("HILLS", 3, 0):
                    new_max_y = y - test_y
                elif chunk.get_tile_type("GROUND0", test_x, test_y) == "PATH":
                    new_max_y = y - test_y - 2
                if new_max_y <= 1: return False

                if "FENCE" == chunk.get_tile_type("FENCE", test_x, test_y) or "WATER" == chunk.get_tile_type("GROUND0", test_x, test_y):
                    return False
        return new_max_y

    def check_house_width():
        test_x = x
        while chunk.has_tile_at_layer("BUILDINGS", test_x, y):  # and not is_special_building(pmap, test_x, y):
            test_x -= 1
        return x - test_x - 1

    def try_build_fence(fx, fy, height, fence):
        if chunk.get_height(fx, fy) == height and chunk.get_tile_type("GROUND0", fx, fy) != "HILLS":  # or chunk.get_tile("GROUND0", fx, fy)[1] == 3):
            chunk.set_tile("FENCE", fx, fy, fence)

    size_x = check_house_width()
    upd_max_y = can_have_fence()
    fence_type = 3 * rel_fence_type
    if upd_max_y:
        fence_height = chunk.get_height(x, y)
        size_y = min(size_x // 2 + 1, max_y, upd_max_y)
        try_build_fence(x, y - size_y, fence_height, Tile("FENCE", 2, 0 + fence_type))
        try_build_fence(x - size_x, y - size_y, fence_height, Tile("FENCE", 0, 0 + fence_type))
        for fence_y in range(y, y - size_y, -1):
            try_build_fence(x - size_x, fence_y, fence_height, Tile("FENCE", 0, 1 + fence_type))
            try_build_fence(x, fence_y, fence_height, Tile("FENCE", 2, 1 + fence_type))
        for fence_x in range(x - size_x + 1, x):
            if tree and random.randint(1, 100) == 1:
                chunk.set_tile("GROUND0", fence_x, y - size_y, Tile("NATURE", 1, 2))
            else:
                try_build_fence(fence_x, y - size_y, fence_height, Tile("FENCE", 1, 0 + fence_type))


# Adds random points to the sides of the map to have path running to the edge of the screen
# def add_random_ends(pmap, path_type):
#     end_sides = []
#     nb_ends = random.randint(2, 4)
#     for end in range(nb_ends):
#         end_side = random.randint(0, 3)
#         while end_side in end_sides:
#             end_side = random.randint(0, 3)
#
#         end_x = 1
#         end_y = 1
#         if end_side == 0:
#             end_x = random.randint(0 + pmap.width // 4, 0 + 3 * (pmap.width // 4))
#             end_sides.append(0)
#         elif end_side == 1:
#             end_x = pmap.width - 1
#             end_y = random.randint(0 + pmap.height // 4, 0 + 3 * (pmap.height // 4))
#             end_sides.append(1)
#         elif end_side == 2:
#             end_x = random.randint(0 + pmap.width // 4, 0 + 3 * (pmap.width // 4))
#             end_y = pmap.height - 1
#             end_sides.append(2)
#         elif end_side == 3:
#             end_y = random.randint(0 + pmap.height // 4, 0 + 3 * (pmap.height // 4))
#             end_sides.append(3)
#
#         max_height = 0
#         for y_around in range(end_y - 2, end_y + 3):
#             for x_around in range(end_x - 3, end_x + 3):
#                 if "fe" == pmap.ground2.get_tile_type((x_around, y_around)):
#                     max_height = -1
#                     break
#                 else:
#                     max_height = max(max_height, pmap.tile_heights.get((x_around, y_around), 0))
#
#         if max_height > 1:
#             pmap.end_points.append((end_x, end_y))
#             pmap.ground.set_tile((end_x, end_y), path_type)
#             for y_around in range(end_y - 2, end_y + 3):
#                 for x_around in range(end_x - 3, end_x + 3):
#                     if not pmap.ground2.out_of_bounds(x_around, y_around) and "wa" != pmap.ground.get_tile_type((x_around, y_around)):
#                         pmap.tile_heights[(x_around, y_around)] = max_height
