import random


# house number/name: (position of upper left corner on the tile sheet), (dimensions of the house measured in tiles), (position of the front door)
house_data = {
    "pokecenter": ((14, 0), (5, 5), (2, 4)),
    "pokemart": ((0, 0), (4, 4), (2, 3)),
    "gym": ((19, 23), (6, 5), (3, 5)),
    0: ((4, 0), (5, 4), (1, 3)),
    1: ((9, 0), (5, 4), (1, 3)),
    2: ((0, 4), (4, 5), (1, 3)),
    3: ((4, 4), (5, 4), (1, 3)),
    4: ((9, 4), (5, 4), (1, 3)),
    5: ((0, 9), (4, 4), (1, 3)),
    6: ((4, 9), (5, 4), (1, 3)),
    7: ((9, 9), (5, 4), (1, 3)),
    8: ((0, 13), (4, 5), (1, 3)),
    9: ((4, 13), (5, 4), (1, 3)),
    10: ((9, 13), (5, 3), (1, 3)),
    11: ((0, 18), (4, 5), (1, 3)),
    12: ((4, 17), (5, 4), (1, 3)),
    13: ((9, 16), (5, 5), (1, 3)),
    14: ((0, 23), (4, 7), (1, 3)),
    15: ((14, 10), (5, 5), (3, 3)),
    16: ((14, 15), (5, 5), (3, 3)),
    17: ((14, 25), (5, 5), (3, 3)),
    18: ((13, 30), (6, 4), (3, 3)),
    19: ((19, 0), (7, 5), (1, 3)),
    20: ((19, 12), (7, 6), (1, 3)),
    21: ((19, 28), (7, 4), (1, 3)),
    "powerplant": ((16, 34), (11, 7), (6, 8))
}


# Spawns a house on the map with house_front_path_type as its front porch
# Houses are spawned by chosing a random x and y coordinate, checking whether enough space is available for the given
# house if not, choose a new position. There's an upper limit to try find a building spot.
def spawn_house(pmap, layer, house_type, path_type):

    # checks if a chosen position has enough free space for the house + spacing, starting from the top left corner
    def unavailable_building_spot(x1, y1, x2, y2):
        reference_height = pmap.tile_heights.get((x1, y1), 0)
        for check_y in range(y1, y2 + 1):
            for check_x in range(x1, x2 + 1):
                if pmap.tile_heights.get((check_x, check_y), -1) != reference_height or "wa" == pmap.ground.get_tile_type((check_x, check_y)) or "fe" == pmap.ground2.get_tile_type((check_x, check_y)) or (check_x, check_y) in layer.get_ex_pos():
                    if layer.get_tile_type((check_x, check_y)):
                        return check_x, check_y
                    else:
                        return True

        return False

    # Chooses a random x and y coordinate to try build a house
    # If a house already exists on the chosen coordinate, searches for the lower right corner of given house and when
    # enough space available, builds the house adjacent on the right to the house previously found
    def search_available_building_spot(cluster_radius, max_attempts):
        attempts = 1
        try_x = random.randint(1, pmap.width - house_size_x)
        try_y = random.randint(1, pmap.height - house_size_y)
        unavailable_spot = unavailable_building_spot(try_x - 2, try_y - 2, try_x + house_size_x + 2, try_y + house_size_y + 2)
        while attempts < max_attempts and unavailable_spot or not is_inside_cluster(pmap, try_x, try_y, cluster_radius, 3):
            attempts += 1
            try_x = random.randint(1, pmap.width - house_size_x)
            try_y = random.randint(1, pmap.height - house_size_y)
            unavailable_spot = unavailable_building_spot(try_x - 2, try_y - 2, try_x + house_size_x + 2, try_y + house_size_y + 2)
            if not isinstance(unavailable_spot, bool):
                lower_right_of_house = find_lower_right_of_house(unavailable_spot[0], unavailable_spot[1], house_size_y)
                try_x, try_y = lower_right_of_house
                unavailable_spot = unavailable_building_spot(try_x, try_y - 2, try_x + house_size_x + 2, try_y + house_size_y + 2)
        return (try_x, try_y) if attempts <= max_attempts and not unavailable_spot and is_inside_cluster(pmap, try_x, try_y, cluster_radius, 3) else False

    # search for the lower right corner of a house
    def find_lower_right_of_house(x, y, size_y):
        while layer.get_tile_type((x - 1, y)) == "ho" or layer.get_tile_type((x, y - 1)) == "ho":
            if layer.get_tile_type((x - 1, y)) == "ho": y += 1
            if layer.get_tile_type((x, y - 1)) == "ho": x += 1
        return x, y - size_y

    curr_data = house_data[house_type]
    house_size_x, house_size_y = house_data[house_type][1]

    map_size_factor = (pmap.buildings.sx * pmap.buildings.sy // 2500) ** 2
    max_attempts = house_size_x * house_size_y * 2 * map_size_factor
    build_spot = search_available_building_spot(40, max_attempts)
    if build_spot:
        house_x = build_spot[0]
        house_y = build_spot[1]
        for house_build_y in range(house_size_y):
            for house_build_x in range(house_size_x):
                layer.set_tile((house_x + house_build_x, house_y + house_build_y), ("ho", curr_data[0][0] + house_build_x, curr_data[0][1] + house_build_y))
        pmap.front_doors.append((round(house_x + house_size_x / 2), house_y + house_size_y + 1))
        for front_y in range(2):
            for front_x in range(house_size_x):
                if (house_x + front_x, house_y + house_size_y + front_y) not in pmap.ground.get_ex_pos():
                    pmap.ground.set_tile((house_x + front_x, house_y + house_size_y + front_y), path_type)
        if isinstance(house_type, int):
            if random.randint(0, 1) == 1 and not (house_x - 1, house_y + house_size_y - 2) in layer.get_ex_pos():
                pmap.ground2.set_tile((house_x - 1, house_y + house_size_y - 2), ("de", 7, 2))
                pmap.ground2.set_tile((house_x - 1, house_y + house_size_y - 1), ("de", 7, 3))

            if random.randint(1, 4) == 1:
                create_fence(pmap, pmap.ground2, house_x + house_size_x - 1, house_y + 1, 5, 1, True)


# Checks whether a coordinate is at least in radius [distance] of [connections] houses
def is_inside_cluster(pmap, x, y, radius, connections):
    from math import sqrt

    if len(pmap.front_doors) == 0:
        return True

    found_connections = 0
    for (front_door_x, front_door_y) in pmap.front_doors:
        if sqrt((x - front_door_x) ** 2 + (y - front_door_y) ** 2) < radius:
            found_connections += 1
        if connections > len(pmap.front_doors):
            if found_connections == 1: return True
        else:
            if found_connections == connections: return True
    return False


def get_house_type(pmap, x, y):
    for house in house_data.keys():
        check_house = pmap.get_tile("buildings", x, y)
        house_type_x, house_type_y = check_house[1], check_house[2]
        curr_house_x, curr_house_y = house_data[house][0]
        curr_house_size_x, curr_house_size_y = house_data[house][1]
        if curr_house_x <= house_type_x < curr_house_x + curr_house_size_x:
            if curr_house_y <= house_type_y < curr_house_y + curr_house_size_y:
                return house
    raise Exception("UnexistingHouse" + str(x, y))


def is_special_building(pmap, x, y):
    return isinstance(get_house_type(pmap, x, y), str)


# gives people a backyard surrounded by a fence
def create_fence(pmap, layer, x, y, max_y, rel_fence_type, tree=False):
    def can_have_fence():
        curr_size = min(size_x // 2 + 1, max_y)
        new_max_y = curr_size
        for test_y in range(y - curr_size - 1, y):
            for test_x in range(x - size_x, x):
                if pmap.ground.get_tile((test_x, test_y)) == ("hi", 3, 0):
                    new_max_y = y - test_y
                elif pmap.ground.get_tile_type((test_x, test_y)) == "pa":
                    new_max_y = y - test_y - 2
                if new_max_y <= 1: return False

                if "fe" == layer.get_tile_type((test_x, test_y)) or "wa" == pmap.ground.get_tile_type((test_x, test_y)):
                    return False
        return new_max_y

    def check_house_width():
        test_x = x
        while "ho" in layer.get_tile_type((test_x, y)) and not is_special_building(pmap, test_x, y):
            test_x -= 1
        return x - test_x - 1

    def try_build_fence(fx, fy, height, fence):
        if pmap.tile_heights.get((fx, fy), -1) == height and (pmap.ground.get_tile_type((fx, fy)) != "hi" or pmap.ground.get_tile((fx, fy))[1] == 3):
            pmap.secondary_ground[(fx, fy)] = fence

    size_x = check_house_width()
    upd_max_y = can_have_fence()
    fence_type = 3 * rel_fence_type
    if upd_max_y:
        fence_height = pmap.tile_heights.get((x, y), -1)
        size_y = min(size_x // 2 + 1, max_y, upd_max_y)
        try_build_fence(x, y - size_y, fence_height, ("fe", 2, 0 + fence_type))
        try_build_fence(x - size_x, y - size_y, fence_height, ("fe", 0, 0 + fence_type))
        for fence_y in range(y, y - size_y, -1):
            try_build_fence(x - size_x, fence_y, fence_height, ("fe", 0, 1 + fence_type))
            try_build_fence(x, fence_y, fence_height, ("fe", 2, 1 + fence_type))
        for fence_x in range(x - size_x + 1, x):
            if tree and random.randint(1, 100) == 1:
                pmap.ground_layer[(fence_x, y - size_y)] = ("na", 1, 2)
            else:
                try_build_fence(fence_x, y - size_y, fence_height, ("fe", 1, 0 + fence_type))


# Adds random points to the sides of the map to have path running to the edge of the screen
def add_random_ends(pmap, path_type):
    end_sides = []
    nb_ends = random.randint(2, 4)
    for end in range(nb_ends):
        end_side = random.randint(0, 3)
        while end_side in end_sides:
            end_side = random.randint(0, 3)

        end_x = 1
        end_y = 1
        if end_side == 0:
            end_x = random.randint(0 + pmap.width // 4, 0 + 3 * (pmap.width // 4))
            end_sides.append(0)
        elif end_side == 1:
            end_x = pmap.width - 1
            end_y = random.randint(0 + pmap.height // 4, 0 + 3 * (pmap.height // 4))
            end_sides.append(1)
        elif end_side == 2:
            end_x = random.randint(0 + pmap.width // 4, 0 + 3 * (pmap.width // 4))
            end_y = pmap.height - 1
            end_sides.append(2)
        elif end_side == 3:
            end_y = random.randint(0 + pmap.height // 4, 0 + 3 * (pmap.height // 4))
            end_sides.append(3)

        max_height = 0
        for y_around in range(end_y - 2, end_y + 3):
            for x_around in range(end_x - 3, end_x + 3):
                if "fe" == pmap.ground2.get_tile_type((x_around, y_around)):
                    max_height = -1
                    break
                else:
                    max_height = max(max_height, pmap.tile_heights.get((x_around, y_around), 0))

        if max_height > 1:
            pmap.end_points.append((end_x, end_y))
            pmap.ground.set_tile((end_x, end_y), path_type)
            for y_around in range(end_y - 2, end_y + 3):
                for x_around in range(end_x - 3, end_x + 3):
                    if not pmap.ground2.out_of_bounds(x_around, y_around) and "wa" != pmap.ground.get_tile_type((x_around, y_around)):
                        pmap.tile_heights[(x_around, y_around)] = max_height