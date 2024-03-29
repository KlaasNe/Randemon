import random
from math import pow
from PIL import Image

from alive_progress import alive_bar
from noise import snoise2

from mapClasses import Map
from mapClasses.Coordinate import Coordinate
from mapClasses.tile.Tile import Tile


def generate_height_map(size_h, size_v, max_height, off_x, off_y, chunk_size, terrain_chaos=4, additional_noise_maps=0,
                        island=False):
    static_offset_array = [(off_x, off_y)]
    for i in range(additional_noise_maps):
        static_offset_array.append((random.randint(0, 1000000), random.randint(0, 1000000)))
    return [
        [(get_height(max_height, x, y, static_offset_array, size_h, size_v, chunk_size, octaves=terrain_chaos,
                     island=island))
         for x in range(size_h)]
        for y in range(size_v)
    ]


def get_height(max_height: int, x: int, y: int, static_offset_array, size_h: int, size_v: int, chunk_size,
               octaves: int = 4, freq: int = 150, island=False):
    def plateau(px: float, py: float, tau: float, height: int, n: float):
        """
        MADE BY HELENA

        geeft de hoogte van een cirkel vormig plateau op (x,y)
        het plateau is van hoogte hoogte
        is nul op r = sqrt(x²+y²) = nulpunt
        tau bepaald hoe scherp de randen van het plateau zijn: hoe kleiner tau hoe scherper
        tau en nulpunt horen altijd groter dan 0 te zijn
        het centrum licht op (0,0)
        """
        r = max(abs(px), abs(py))
        return height * (1 - pow(2.71, -(r + n) / tau)) * (1 - pow(2.71, (r - n) / tau))

    if island and (x == 0 or y == 0 or x == size_h - 1 or y == size_v - 1):
        return -1
    noise = 0
    total_noise_maps = len(static_offset_array)
    tuple_count = 1
    for offset_tuple in static_offset_array:
        off_x, off_y = offset_tuple
        noise += snoise2(
            (off_x + x) / (freq * tuple_count),
            (off_y + y) / (freq * tuple_count),
            octaves) / tuple_count
        tuple_count += 1
    # if total_noise_maps > 1:
    #     noise /= sum(1 / i for i in range(1, total_noise_maps + 1))
    if island:
        # print(noise*max_height)
        return (noise * (max_height + 2)) + plateau((x - (size_h // 2)) / (size_h / 2), (y - (size_v // 2)) / (size_v / 2),
                                              0.15, 1, 0.5)  # GEEN 0 invullen op height plateau!!!
    else:
        elevation = noise + 0.45
        return elevation * max_height


def generate_height_map_from_image(img_path):
    im = Image.open(img_path)
    width, height = im.width, im.height
    image_array = list(im.getdata())
    height_map = []
    for y in range(height):
        height_map_row = []
        for x in range(width):
            height_map_row.append(image_array[y * width + x][0] // 10 - 1)
        height_map.append(height_map_row)
    return height_map


def smooth_height(rmap: Map) -> None:
    smooth = False
    tries = 0
    while not smooth:
        smooth = True
        tries += 1
        heights_sorted = dict()
        for y in range(0, rmap.size_v):
            for x in range(0, rmap.size_h):
                h = round(rmap.get_height_map_pos(x, y))
                if h > 0:
                    if h in heights_sorted.keys():
                        heights_sorted[h].append((x, y))
                    else:
                        heights_sorted[h] = [(x, y)]
        heights_sorted = dict(reversed(sorted(heights_sorted.items())))
        steps = 0
        for h in heights_sorted.values():
            steps += len(h)

        with alive_bar(steps, title=f"smoothening terrain | attempt {tries}", theme="classic") as smooth_bar:
            for h in heights_sorted.values():
                for x, y in h:
                    if rmap.height_map[y][x] > 0:
                        if not smooth_down(rmap, x, y):
                            smooth = False
                    smooth_bar()


def smooth_down(rmap: Map, x: int, y: int) -> bool:
    def check_and_update_height(u_x, u_y):
        if rmap.in_bounds(u_x, u_y) and height_diff > 1:
            rmap.height_map[u_y][u_x] = center_height + 1
            return set(Coordinate(u_x, u_y).around())
        elif rmap.in_bounds(u_x, u_y) and height_diff < -1:
            rmap.height_map[u_y][u_x] = center_height - 1
            return set(Coordinate(u_x, u_y).around())

    center_height: int = rmap.height_map[y][x]
    tile_updates: list[tuple] = list()
    updated_tiles: list[tuple] = list()
    smooth = True
    for test_y in range(max(0, y - 1), min(y + 2, rmap.size_v)):
        for test_x in range(max(0, x - 1), min(x + 2, rmap.size_h)):
            test_height = max(0, rmap.get_height_map_pos(test_x, test_y))
            height_diff = test_height - center_height
            tiles_to_check = check_and_update_height(test_x, test_y)
            if tiles_to_check is not None:
                smooth = False
                tile_updates += tiles_to_check
                while tile_updates:
                    update_x, update_y = tile_updates.pop()
                    updated_tiles.append((update_x, update_y))
                    tiles_to_check = check_and_update_height(update_x, update_y)
                    if tiles_to_check is not None:
                        tile_updates = list(set(tile_updates).difference(updated_tiles))
    return smooth


def draw_height_map(rmap: Map, chunk):
    for y in range(chunk.size):
        for x in range(chunk.size):
            chunk.set_tile("HEIGHTMAP", x, y, Tile("HEIGHTS", round(rmap.get_height(chunk, x, y)), 0))
