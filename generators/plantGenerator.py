import random

from noise import snoise2

from mapClasses.chunk import Chunk
from mapClasses.tile import Tile


octaves1 = 2
freq1 = 40
octaves2 = 1
freq2 = 200
octaves3 = 4
freq3 = 100

max_height = 3


# Checks if enough space is available to plant a tree
# No trees above the highest path height
# Adds an overlay to decoration_layer if the top of the tree overlaps with another tree
def create_trees(chunk: Chunk, spawn_rate):
    double = False
    for y in range(chunk.size):
        for x in range(chunk.size):
            if max_height > chunk.get_height_exact(x, y) > 0.75:
                # if chunk.tile_heights.get((x, y), -1) <= chunk.highest_path:
                if not chunk.has_tile_in_layer_at("GROUND0", x, y) and not chunk.has_tile_in_layer_at("BUILDINGS", x, y) and not chunk.has_tile_in_layer_at("HILLS", x, y) \
                        and not chunk.has_tile_in_layer_at("GROUND1", x, y - 1) \
                        and not chunk.has_tile_in_layer_at("GROUND2", x, y) and not chunk.has_tile_in_layer_at("GROUND2", x, y - 1) and not chunk.has_tile_in_layer_at("GROUND2", x, y - 2)\
                        and not chunk.has_tile_in_layer_at("FENCE", x, y)\
                        and not chunk.out_of_bounds(x, y) and not chunk.out_of_bounds(x, y - 1 and not chunk.out_of_bounds(x, y - 2)):
                    if random.random() > 0.3 and tree_formula(chunk, x, y) > 1 - spawn_rate:
                        if double:
                            chunk.set_tile("GROUND2", x - 1, y - 2, Tile("NATURE", 1, 5))
                            chunk.set_tile("GROUND2", x, y - 2, Tile("NATURE", 2, 5))
                            chunk.set_tile("GROUND1", x - 1, y - 1, Tile("NATURE", 1, 6))
                            chunk.set_tile("GROUND1", x, y - 1, Tile("NATURE", 2, 6))
                            chunk.set_tile("GROUND0", x - 1, y, Tile("NATURE", 1, 7))
                            chunk.set_tile("GROUND0", x, y, Tile("NATURE", 2, 7))
                            double = False
                        else:
                            chunk.set_tile("GROUND2", x, y - 2, Tile("NATURE", 2, 0))
                            chunk.set_tile("GROUND1", x, y - 1, Tile("NATURE", 2, 1))
                            chunk.set_tile("GROUND0", x, y, Tile("NATURE", 2, 2))
                            double = True
                    else:
                        double = False
                else:
                    double = False
            else:
                double = False


def tree_formula(chunk, x, y):
    return abs(snoise2((x + chunk.off_x) / freq1, (y + chunk.off_y) / freq1, octaves1)
               + snoise2((x + chunk.off_x) / freq2, (y + chunk.off_y) / freq2, octaves2)
               - abs(snoise2((x + chunk.off_x) / freq3, (y + chunk.off_y) / freq3, octaves3))
               )


# The whole map is filled with random green tiles
# Tall gras and flowers are spawned with a perlin noise field
def grow_grass(chunk, coverage):
    octaves = 2
    freq = 10 * octaves
    for y in range(chunk.size):
        for x in range(chunk.size):
            if not chunk.has_tile_in_layer_at("GROUND0", x, y):
                sne_prob = abs(snoise2((x + chunk.off_x) / freq, (y + chunk.off_y) / freq, octaves))
                if not chunk.has_town:
                    tile_height = chunk.get_height(x, y)
                    if tile_height <= max_height:
                        tile = random_tall_grass() if sne_prob >= 1 - coverage else random_grass()
                    else:
                        hill_tile = chunk.get_tile("HILLS", x, y)
                        if True: # hill_tile and tile_height == max_height + 1 and hill_tile != Tile("HILLS", 3, 0):
                            tile = random_grass()
                        else:
                            tile = Tile("HILLS", 0, 0)
                else:
                    tile = random_grass()
                chunk.set_tile("GROUND0", x, y, tile)


def random_grass():
    return Tile("NATURE", 0, random.randint(0, 7)) if random.random() < 0.99 else Tile("NATURE", 2, 3)


def random_tall_grass():
    sne_type = random.randint(0, 1)
    # Turn 85 percent of the flowers into tall grass
    if sne_type == 1 and random.random() < 0.85:
        return Tile("NATURE", 1, 0)
    # Turn 0.5 percent of the tall grass into tall grass with a hidden item
    elif sne_type == 0 and random.random() < 0.005:
        return Tile("NATURE", 1, 4)
    return Tile("NATURE", 1, sne_type)


# # Creates an overlay for the entire map showing rain
# # The amount of rain is given with rain_rate
# def create_rain(pmap, layer, odds, rain_rate):
#     if random.random() < odds:
#         for y in range(pmap.height):
#             for x in range(pmap.width):
#                 if random.random() < rain_rate:
#                     if random.random() < 0.5 and "fe" != pmap.ground2.get_tile_type(
#                             (x, y)) and "hi" != pmap.ground.get_tile_type((x, y)) and (
#                     x, y) not in pmap.npc.get_ex_pos():
#                         layer.set_tile((x, y), ("ra", random.randint(0, 2), 1))
#                     else:
#                         layer.set_tile((x, y), ("ra", random.randint(1, 2), 0))
#                 else:
#                     layer.set_tile((x, y), ("ra", 0, 0))
