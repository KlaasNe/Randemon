from math import floor

from noise import snoise2


octaves = 2
freq = 25 * octaves


# Creates a perlin noise field to be used as height map with ints as height ranging from 0 to pmap.max_hill_height
def generate_height_map(size, max_height, off_x, off_y):
    height_map = [[0 for x in range(size)] for y in range(size)]
    for y in range(size):
        for x in range(size):
            noise = snoise2(((x + off_x) // 4) / freq, ((y + off_y) // 4) / freq, octaves)
            height_map[y][x] = int(abs(floor(noise * max_height + 1)))
    return height_map


def get_height(max_height, off_x, off_y):
    noise = snoise2((off_x // 4) / freq, (off_y // 4) / freq, octaves)
    return int(abs(floor(noise * max_height + 1)))
