import random
from math import sqrt

# Spawns a house on the map with house_front_path_type as its front porch
# Houses are spawned by chosing a random x and y coordinate, checking whether enough space is available for the given
# house if not, choose a new position. There's an upper limit to try find a building spot.
from buildings.Building import Building
from buildings.BuildingTypes import BuildingTypes
from mapClasses import Tile


def spawn_building(chunk, building, path_type):
    # checks if a chosen position has enough free space for the house + spacing, starting from the top left corner
    def is_available_spot(x1, y1, x2, y2):
        reference_height = chunk.get_height(x1, y1, 0)
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if chunk.out_of_bounds(x, y) or chunk.get_height(x, y) != reference_height or (x, y) in chunk.get_ex_pos("GROUND0") or (x, y) in chunk.get_ex_pos("HILLS") or (x, y) in chunk.get_ex_pos("BUILDINGS"):
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
    map_size_factor = (chunk.size * chunk.size // 2500) ** 2
    max_attempts = size_x * size_y * 2 * map_size_factor
    build_spot = search_available_spot(building, 30, max_attempts)
    if build_spot:
        house_x, house_y = build_spot
        for house_build_y in range(size_y):
            for house_build_x in range(size_x):
                chunk.set_tile("BUILDINGS", house_x + house_build_x, house_y + house_build_y,
                               Tile("BUILDINGS", building.t_pos[0] + house_build_x, building.t_pos[1] + house_build_y))
        chunk.buildings.append(Building(building, build_spot[0], build_spot[1]))
        for front_y in range(2):
            for front_x in range(size_x):
                chunk.set_tile("GROUND0", house_x + front_x, house_y + size_y + front_y, Tile("PATH", 0, 0))
        # if isinstance(building, int):
        #     if random.randint(0, 1) == 1 and not (house_x - 1, house_y + size_y - 2) in chunk.get_layer("BUILDINGS").get_ex_pos():
        #         chunk.ground2.set_tile((house_x - 1, house_y + size_y - 2), ("de", 7, 2))
        #         chunk.ground2.set_tile((house_x - 1, house_y + size_y - 1), ("de", 7, 3))

        # if random.randint(1, 4) == 1:
        #     create_fence(chunk, chunk.ground2, house_x + size_x - 1, house_y + 1, 5, 1, True)


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
            if found_connections == 1:
                return True
        else:
            if found_connections == connections:
                return True
    return False


def spawn_functional_buildings(chunk, path_type):
    spawn_building(chunk, BuildingTypes.POKECENTER.value, "p1")
    spawn_building(chunk, BuildingTypes.GYM.value, "p1")
    spawn_building(chunk, BuildingTypes.POKEMART.value, "p1")


# def is_special_building(pmap, x, y):
#     return isinstance(get_house_type(pmap, x, y), str)


# gives people a backyard surrounded by a fence
# def create_fence(pmap, layer, x, y, max_y, rel_fence_type, tree=False):
#     def can_have_fence():
#         curr_size = min(size_x // 2 + 1, max_y)
#         new_max_y = curr_size
#         for test_y in range(y - curr_size - 1, y):
#             for test_x in range(x - size_x, x):
#                 if pmap.ground.get_tile((test_x, test_y)) == ("hi", 3, 0):
#                     new_max_y = y - test_y
#                 elif pmap.ground.get_tile_type((test_x, test_y)) == "pa":
#                     new_max_y = y - test_y - 2
#                 if new_max_y <= 1: return False
#
#                 if "fe" == layer.get_tile_type((test_x, test_y)) or "wa" == pmap.ground.get_tile_type((test_x, test_y)):
#                     return False
#         return new_max_y
#
#     def check_house_width():
#         test_x = x
#         while "ho" in layer.get_tile_type((test_x, y)):  # and not is_special_building(pmap, test_x, y):
#             test_x -= 1
#         return x - test_x - 1
#
#     def try_build_fence(fx, fy, height, fence):
#         if pmap.tile_heights.get((fx, fy), -1) == height and (pmap.ground.get_tile_type((fx, fy)) != "hi" or pmap.ground.get_tile((fx, fy))[1] == 3):
#             pmap.secondary_ground[(fx, fy)] = fence
#
#     size_x = check_house_width()
#     upd_max_y = can_have_fence()
#     fence_type = 3 * rel_fence_type
#     if upd_max_y:
#         fence_height = pmap.tile_heights.get((x, y), -1)
#         size_y = min(size_x // 2 + 1, max_y, upd_max_y)
#         try_build_fence(x, y - size_y, fence_height, ("fe", 2, 0 + fence_type))
#         try_build_fence(x - size_x, y - size_y, fence_height, ("fe", 0, 0 + fence_type))
#         for fence_y in range(y, y - size_y, -1):
#             try_build_fence(x - size_x, fence_y, fence_height, ("fe", 0, 1 + fence_type))
#             try_build_fence(x, fence_y, fence_height, ("fe", 2, 1 + fence_type))
#         for fence_x in range(x - size_x + 1, x):
#             if tree and random.randint(1, 100) == 1:
#                 pmap.ground_layer[(fence_x, y - size_y)] = ("na", 1, 2)
#             else:
#                 try_build_fence(fence_x, y - size_y, fence_height, ("fe", 1, 0 + fence_type))


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
