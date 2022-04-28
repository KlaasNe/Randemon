from math import floor
import random

from noise import snoise2

from mapClasses.tile.Tile import Tile

octaves = 2
freq = 25 * octaves


def generate_height_map(size_h, size_v, max_height, off_x, off_y):
    return [[get_height(max_height, off_x + x, off_y + y) for x in range(size_h)] for y in range(size_v)]


def get_height(max_height, off_x, off_y):
    noise = snoise2((off_x // 4) / freq, (off_y // 4) / freq, octaves)
    return int(abs(floor(noise * max_height + 1)))


def add_island_mask(rmap, min_mask, max_mask):
    size_h, size_v = rmap.size_h, rmap.size_v
    mask_range = list(range(min_mask, max_mask + 1))
    mask_range.reverse()
    y = 0
    for row in rmap.height_map:
        for x in range(len(row)):
            dist = max(round(abs(x - size_h // 2) / (size_h / (max_mask - min_mask)) * 2),
                       round(abs(y - size_v // 2) / (size_v / (max_mask - min_mask)) * 2))
            mask = mask_range[dist]
            row[x] = max(0, round(row[x] + mask))
        y += 1


def smooth_height(rmap, down=False, radius=4):
    smooth = False
    while not smooth:
        smooth = True
        for y in range(rmap.size_v):
            for x in range(rmap.size_h):
                smooth_tile = smooth_down(rmap, x, y, radius=radius) if down else smooth_up(rmap, x, y, radius=radius)
                if not smooth_tile:
                    smooth = False


def smooth_down(rmap, x, y, radius=1):
    center_height = rmap.height_map[y][x]
    for test_y in range(y - radius, y + radius + 1):
        for test_x in range(x - radius, x + radius + 1):
            try:
                test_height = rmap.height_map[test_y][test_x]
                if center_height - test_height > 1:
                    rmap.height_map[y][x] = test_height + 1
                    return False
            except IndexError:
                pass
    return True


def smooth_up(rmap, x, y, radius=1):
    center_height = rmap.height_map[y][x]
    for test_y in range(y - radius, y + radius + 1):
        for test_x in range(x - radius, x + radius + 1):
            try:
                test_height = rmap.height_map[test_y][test_x]
                if center_height - test_height > 1:
                    rmap.height_map[test_y][test_x] = center_height - 1
                    return False
            except IndexError:
                pass
    return True


def draw_height_map(rmap, chunk):
    for y in range(chunk.size):
        for x in range(chunk.size):
            chunk.set_tile("HEIGHTMAP", x, y, Tile("HEIGHTS", rmap.get_height(chunk, x, y), 0))
