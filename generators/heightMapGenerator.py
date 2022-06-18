from math import floor, sqrt
from PIL import Image

from alive_progress import alive_bar
from noise import snoise2

from mapClasses.tile.Tile import Tile


def generate_height_map(size_h, size_v, max_height, off_x, off_y):
    return [[get_height(max_height, off_x + x, off_y + y) for x in range(size_h)] for y in range(size_v)]


def get_height(max_height, off_x, off_y, cool=True):
    octaves = 1
    freq = 100
    noise = max_height * snoise2((off_x // 4) / freq, (off_y // 4) / freq, octaves)
    noise2 = max_height / 2 * snoise2((off_x // 4) * 2 / freq, (off_y // 4) * 2 / freq, octaves)
    noise3 = max_height / 4 * snoise2((off_x // 4) * 4 / freq, (off_y // 4) * 4 / freq, octaves)
    return abs(floor(noise + noise2 + noise3)) - 1


def generate_height_map_from_image(img_path):
    im = Image.open(img_path)
    width, height = im.size
    image_array = list(im.getdata())
    height_map = []
    for y in range(height):
        height_map_row = []
        for x in range(width):
            height_map_row.append(image_array[y * width + x][0] // 10 - 1)
        height_map.append(height_map_row)

    return height_map


def add_island_mask(rmap, max_height, off_x, off_y, mask_type="circle", mask_range=None, custom_range=None, strict=True):
    if mask_range is None: mask_range = (-max_height * 2 - 1, max_height) if strict else (-max_height, max_height)
    size_h, size_v = rmap.size_h, rmap.size_v
    if custom_range is None:
        min_mask, max_mask = mask_range[0], mask_range[1]
        mask = list(range(min_mask, max_mask + 1))
    else:
        mask = custom_range
    mask.reverse()
    y = 0
    octaves = 1
    freq = 50
    if mask_type == "circle":
        for row in rmap.height_map:
            for x in range(len(row)):
                dist = max(round(sqrt(((x - size_h // 2)//4*4)**2 + ((y - size_v // 2)//4*4)**2) // 1.5 / (size_h / (len(mask) - 1)) * 2),
                           round(sqrt(((x - size_h // 2)//4*4)**2 + ((y - size_v // 2)//4*4)**2) // 1.5 / (size_v / (len(mask) - 1)) * 2))
                mask_val = mask[dist]
                row[x] = max(-1, round(row[x] + mask_val))
            y += 1
    elif mask_type == "square":
        for row in rmap.height_map:
            for x in range(len(row)):
                dist = max(round(abs(x - size_h // 2) / (size_h / (len(mask) - 1)) * 2),
                           round(abs(y - size_v // 2) / (size_v / (len(mask) - 1)) * 2))
                noise = round(snoise2(((off_x + x) // 4) / freq, ((off_y + y) // 4) / freq, octaves) * max_height) * 2
                mask_val = mask[dist] + noise
                row[x] = max(-1, round(row[x] + mask_val))
            y += 1


def smooth_height(rmap, radius=1):
    smooth = False
    max_progress = 0
    with alive_bar(rmap.size_v * rmap.size_h // radius ** 2, title="smoothening terrain", theme="classic") as smooth_bar:
        while not smooth:
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
    min_height = center_height
    for test_y in range(max(0, y - radius), min(y + radius + 1, rmap.size_v)):
        for test_x in range(max(0, x - radius), min(x + radius + 1, rmap.size_h)):
            min_height = max(0, min(min_height, rmap.height_map[test_y][test_x]))
    for test_y in range(max(0, y - radius), min(y + radius + 1, rmap.size_v)):
        for test_x in range(max(0, x - radius), min(x + radius + 1, rmap.size_h)):
            test_height = max(0, rmap.height_map[test_y][test_x])
            if test_height - min_height > 1:
                rmap.height_map[test_y][test_x] = min_height + 1
                smooth = False
    return smooth


def draw_height_map(rmap, chunk):
    for y in range(chunk.size):
        for x in range(chunk.size):
            chunk.set_tile("HEIGHTMAP", x, y, Tile("HEIGHTS", rmap.get_height(chunk, x, y), 0))
