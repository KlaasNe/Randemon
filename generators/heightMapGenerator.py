from math import floor

from noise import snoise2


# Creates a perlin noise field to be used as height map with ints as height ranging from 0 to pmap.max_hill_height
def generate_height_map(size, max_height, off_x, off_y):
    height_map = [[0 for x in range(size)] for y in range(size)]
    octaves = 2
    freq = 25 * octaves
    for y in range(size):
        for x in range(size):
            noise = snoise2((x // 4 + off_x) / freq, (y // 4 + off_y) / freq, octaves)
            height_map[y][x] = int(abs(floor(noise * max_height + 1)))
    return height_map
