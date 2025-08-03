import numpy as np
from noise import snoise2


class HeightMap:

    def __init__(self, shape, chunk_size, random_x_offset, random_y_offset, max_height, island=False):
        self.shape = shape[0] * chunk_size, shape[1] * chunk_size
        self.height_matrix: np.array = np.zeros(self.shape, dtype=float)
        for y in range(self.shape[1]):
            for x in range(self.shape[0]):
                self.height_matrix[y][x] = HeightMap.get_height(max_height, x, y, random_x_offset, random_y_offset, (self.shape[0], self.shape[1]), island)

    def __getitem__(self, row):
        return self.height_matrix[row]

    @staticmethod
    def get_height(max_height: int, x: int, y: int, random_x_offset: int, random_y_offset: int, shape, island,
                   octaves: int = 6, freq: int = 150):

        size_h, size_v = shape
        if island and (x == 0 or y == 0 or x == size_h - 1 or y == size_v - 1):
            return -1
        noise = snoise2(
            (random_x_offset + x) / freq,
            (random_y_offset + y) / freq,
            octaves, persistence=0.5, lacunarity=1.6)
        if island:
            return (noise * (max_height + 2)) + HeightMap.plateau((x - (size_h // 2)) / (size_h / 2),
                                                        (y - (size_v // 2)) / (size_v / 2), 0.20, 1,
                                                        0.5)  # GEEN 0 invullen op height plateau!!!
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
