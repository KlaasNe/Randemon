import random
from math import pow
from PIL import Image

from alive_progress import alive_bar
from noise import snoise2

from mapClasses.tile.Tile import Tile


def generate_height_map(size_h, size_v, max_height, off_x, off_y, additional_noise_maps=0, island=False):
    static_offset_array = [(off_x, off_y)]
    for i in range(additional_noise_maps):
        static_offset_array.append((random.randint(0, 1000000), random.randint(0, 1000000)))
    return [
        [(get_height(max_height, x, y, static_offset_array, size_h, size_v, island=island, flattening=2)) for x in range(size_h)]
        for y in range(size_v)
    ]


def get_height(max_height, x, y, static_offset_array, size_h, size_v, octaves=4, freq=150, island=False, flattening=2):
    if island and (x == 0 or y == 0 or x == size_h - 1 or y == size_v - 1):
        return 0
    noise = 0
    total_noise_maps = len(static_offset_array)
    tuple_count = 1
    for offset_tuple in static_offset_array:
        off_x, off_y = offset_tuple
        noise += (1 / tuple_count) * snoise2(
            (off_x + x) / freq,
            (off_y + y) / freq,
            octaves)
        tuple_count += 1
    if total_noise_maps > 1:
        noise /= sum(1 / i for i in range(1, total_noise_maps + 1))
    if island:
        nx = 2 * x / size_h - 1
        ny = 2 * y / size_v - 1
        d = 1 - (1 - nx ** 2) * (1 - ny ** 2)
        elevation = (noise + (1 - d)) / flattening
    else:
        elevation = noise + 0.45
    return max(0, pow(elevation, 3) * max_height * 2)


def generate_height_map_from_image(img_path):
    im = Image.open(img_path)
    width, height = im.chunk_size
    image_array = list(im.getdata())
    height_map = []
    for y in range(height):
        height_map_row = []
        for x in range(width):
            height_map_row.append(image_array[y * width + x][0] // 10 - 1)
        height_map.append(height_map_row)

    return height_map


def smooth_height(rmap, radius=1):
    smooth = False
    max_progress = 0
    tries = 0
    with alive_bar(rmap.size_v * rmap.size_h // radius ** 2, title="smoothening terrain",
                   theme="classic") as smooth_bar:
        while not smooth and tries < 10:
            tries += 1
            smooth = True
            progress = 0
            for y in range(0, rmap.size_v, radius):
                for x in range(0, rmap.size_h, radius):
                    if rmap.height_map[y][x] > 0:
                        smooth_tile = smooth_down(rmap, x, y, radius=radius)
                        if not smooth_tile:
                            smooth = False
                    progress += 1
                    if smooth and progress > max_progress:
                        smooth_bar()
                        max_progress = progress


def smooth_down(rmap, x, y, radius=1):
    smooth = True
    center_height = rmap.height_map[y][x]
    # min_height = center_height
    # max_height = center_height
    # for test_y in range(max(0, y - radius), min(y + radius + 1, rmap.size_v)):
    #     for test_x in range(max(0, x - radius), min(x + radius + 1, rmap.size_h)):
    #         test_height = rmap.height_map[test_y][test_x]
    #         min_height = max(0, min(min_height, test_height))
    #         max_height = max(max_height, test_height)
    #         avg_height = (min_height + max_height) / 2
    for test_y in range(max(0, y - radius), min(y + radius + 1, rmap.size_v)):
        for test_x in range(max(0, x - radius), min(x + radius + 1, rmap.size_h)):
            test_height = max(0, rmap.height_map[test_y][test_x])
            height_diff = test_height - center_height
            if height_diff > 1:
                rmap.height_map[test_y][test_x] = center_height + 1
                smooth = False
            elif height_diff < -1:
                rmap.height_map[test_y][test_x] = center_height - 1
                smooth = False
    return smooth


def draw_height_map(rmap, chunk):
    for y in range(chunk.size):
        for x in range(chunk.size):
            chunk.set_tile("HEIGHTMAP", x, y, Tile("HEIGHTS", rmap.get_height(chunk, x, y), 0))
