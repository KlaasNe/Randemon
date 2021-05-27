import random
from generators.pathGenerator import is_actual_path, get_path_type
from generators.buildingGenerator import is_inside_cluster

# Lists of sprite numbers which can be spawned at certain locations
NB_NPC = 55  # The amount of different npcs
off_Path_Npc = [1, 17, 20, 21, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45]  # Npcs to be spawned off path
water_Npc = [34, 35, 36]  # Npcs to be spawned in water
shore_Npc = [31, 32, 37, 38]  # Npcs to be spawned on beach
bridge_Npc = [37, 38, 42, 43, 44]  # Npcs to be spawned on a bridge
outside_Npc = [1, 17, 20, 21, 45]  # Npcs to be spawned outside on grass, not on path


# Spawn npc over the map
# If path_only is set to True, npcs will only spawn on path
def spawn_npc(pmap, layer, population, path_only=False):
    coord = random_npc_coordinates(pmap, population)
    for co in coord:
        x, y = co
        if pmap.tile_heights.get((x, y), -1) <= pmap.highest_path and (x, y) not in pmap.buildings.get_ex_pos() and "hi" != pmap.ground.get_tile_type((x, y)) and (x, y) not in pmap.ground2.get_ex_pos():
            if path_only:
                if is_actual_path(pmap.ground, x, y):
                    npc = get_path_npc()
                    set_npc(layer, npc, x, y)
            else:
                npc = get_npc(pmap, x, y)
                if npc is not None:
                    set_npc(pmap, pmap.npc, npc, x, y)


# Spawns an npc on a given set of coordinates, each npc looking at a certain direction
# If an npc is looking to the right (direction == 2), another npc can be spawned adjacent to previous looking at them
# as if they're talking
def set_npc(pmap, layer, npc, x, y):
    direction = 0 if npc == 54 else random.randint(0, 3)  # Npcs nr 50 only has 1 direction
    layer.set_tile((x, y), ("np", npc % 5 * 4 + direction, npc // 5))
    if direction == 1 and is_actual_path(pmap.ground, x, y):
        if (x + 1, y) not in layer.get_ex_pos() and (x + 1, y) not in pmap.buildings.get_ex_pos() and "hi" != pmap.ground.get_tile((x + 1, y)) and "fe" != pmap.ground.get_tile(x + 1, y) and (x + 1, y) not in pmap.ground2.get_ex_pos():
            snpc = get_path_npc()
            while snpc == 54:
                snpc = get_path_npc()
            layer.set_tile((x + 1, y), ("np", snpc % 5 * 4 + 3, snpc // 5))


# Determines what kind of npc should be spawned on a certain set of coordinates
def get_npc(pmap, x, y):
    WATER_LVL = 0.2
    npc_number = None
    if not pmap.raining:
        if random.random() < WATER_LVL and "wa" == pmap.ground.get_tile_type((x, y)) and is_inside_cluster(pmap, x, y, 8, 1):
            npc_number = get_water_npc()
        elif "ro" == pmap.ground.get_tile((x, y)):
            npc_number = get_bridge_npc()
        elif random.random() < WATER_LVL and 3 == get_path_type(pmap.ground, x, y) in pmap.ground.get_tile((x, y)) and is_inside_cluster(pmap, x, y, 8, 1):
            npc_number = get_shore_npc()
    if (x, y) not in pmap.ground.get_ex_pos():
        npc_number = get_outside_npc()
    elif is_actual_path(pmap.ground, x, y):
        npc_number = get_path_npc()
    return npc_number


# Picks a random npc number for path npc
def get_path_npc():
    npc_nr = random.randint(1, NB_NPC)
    while npc_nr in off_Path_Npc:
        npc_nr = random.randint(1, NB_NPC)
    return npc_nr


# Picks a random npc number for water npc
def get_water_npc():
    return water_Npc[random.randint(1, len(water_Npc) - 1)]


# Picks a random npc number for bridge npc
def get_bridge_npc():
    return bridge_Npc[random.randint(1, len(bridge_Npc) - 1)]


# Picks a random npc number for beach npc
def get_shore_npc():
    return shore_Npc[random.randint(1, len(shore_Npc) - 1)]


# Picks a random npc number for outside npc
def get_outside_npc():
    return outside_Npc[random.randint(1, len(outside_Npc) - 1)]


# Creates a set of coordinates on the map where to spawn npcs if possible
# population is the percentage of the map to be covered by npcs
def random_npc_coordinates(pmap, population):
    coord = set()
    for npc in range(round(pmap.width * pmap.height * (population / 100))):
        (x, y) = random_on_map(pmap)
        coord.add((x, y))
    return coord


# Returns random coordinates inside the boundaries of the given map
def random_on_map(pmap):
    return random.randint(0, pmap.width - 1), random.randint(0, pmap.height - 1)
