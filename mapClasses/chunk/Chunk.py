from generators.heightMapGenerator import generate_height_map
from mapClasses.layer import *


class Chunk:

    def __init__(self, size, off_x, off_y):
        self.size = size
        self.off_x = off_x
        self.off_y = off_y
        self.layers = dict()
        for layer in Layers:
            self.layers[layer.name] = Layer()
        self.height_map = generate_height_map(self.size, 4, self.off_x, self.off_y)
        self.buildings = []

    def get_layer(self, layer):
        return self.layers[layer]

    def get_tile(self, layer, x, y):
        return self.get_layer(layer).get_tile(x, y)

    def set_tile(self, layer, x, y, tile):
        self.get_layer(layer).set_tile(x, y, tile)

    def has_tile_at(self, x, y):
        for layer in self.layers.values():
            if layer.get_tile(x, y) is not None:
                return True
        return False

    def get_height(self, x, y, default=0):
        try:
            return self.height_map[y][x] if x >= 0 and y >= 0 else default
        except IndexError:
            return default

    def get_ex_pos(self, layer):
        return self.get_layer(layer).get_ex_pos()

    def get_tile_type(self, layer, x, y):
        return self.get_layer(layer).get_tile_type(x, y)

    def out_of_bounds(self, x, y):
        return not (0 <= x < self.size and 0 <= y < self.size)
