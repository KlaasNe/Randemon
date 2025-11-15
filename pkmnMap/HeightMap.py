import math

import numpy as np
from noise import snoise2

from timeit import timeit


class HeightMap:

    def __init__(self, shape, chunk_size, random_x_offset, random_y_offset, max_height, elevation=4.0, island=False):
        self.shape = shape[0] * chunk_size, shape[1] * chunk_size
        self.height_matrix: np.array = np.zeros(self.shape, dtype=float)
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                self.height_matrix[y][x] = HeightMap.find_height(max_height, x, y, random_x_offset, random_y_offset,
                                                                 (self.shape[0], self.shape[1]), island,
                                                                 elevation=elevation)

    def __getitem__(self, row):
        return self.height_matrix[row]

    @timeit
    def smooth(self, radius: int) -> "HeightMap":
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                total_height = 0
                tile_count = 0
                for ry in range(max(0, y - radius), min(y + radius, self.shape[1])):
                    for rx in range(max(0, x - radius), min(x + radius, self.shape[0])):
                        if math.dist((rx, ry), (x, y)) <= radius:
                            h = self[y][x]
                            total_height += h if h > -1 else -1
                            tile_count += 1

                avg_height = total_height / tile_count
                self[y][x] = avg_height

        return self

    @timeit
    def remove_faulty_heights(self) -> "HeightMap":
        for y in range(1, self.shape[1] - 1):
            for x in range(1, self.shape[0] - 1):
                h = self[y][x]
                up = self[y - 1][x]
                down = self[y + 1][x]
                left = self[y][x - 1]
                right = self[y][x + 1]

                if abs(round(h) - round(up)) >= 1 and abs(round(h) - round(down)) >= 1:
                    self[y][x] = (up + down) / 2
                elif abs(round(h) - round(left)) >= 1 and abs(round(h) - round(right)) >= 1:
                    self[y][x] = (left + right) / 2

        return self

    @timeit
    def erode(self, ):
        ...

    @staticmethod
    def find_height(max_height: int, x: int, y: int, random_x_offset: int, random_y_offset: int, shape, island,
                    octaves: int = 6, freq: int = 150, elevation: float = 0.0):

        size_h, size_v = shape
        if island and (x == 0 or y == 0 or x == size_h - 1 or y == size_v - 1):
            return -1
        noise = snoise2(
            (random_x_offset + x) / freq,
            (random_y_offset + y) / freq,
            octaves, persistence=0.5, lacunarity=1.6)
        if island:
            return (noise * max_height) + (1 - (math.dist((x, y), (size_h // 2, size_v // 2)) / size_h)) * 6 - 4 + HeightMap.plateau(
                (x - (size_h // 2)) / (size_h / 2), (y - (size_v // 2)) / (size_v / 2), .2, 1,
                0.5) + elevation  # GEEN 0 invullen op height plateau!!!
        else:
            elevation = noise + .45  # TODO ???? magic number??? why????
            return elevation * max_height

    @staticmethod
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
