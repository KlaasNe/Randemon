from generators.heightMapGenerator import get_height
from mapClasses.layer import *

MAX_HEIGHT = 5


class Chunk:

    def __init__(self, pmap, size, chunk_x, chunk_y, off_x, off_y):
        self.map = pmap
        self.size = size
        self.off_x = off_x
        self.off_y = off_y
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.layers = dict()
        for layer in Layers:
            self.layers[layer.name] = Layer()
        self.buildings = []
        self.has_town = False

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

    def has_tile_at_layer(self, layer, x, y):
        return self.get_tile(layer, x, y) is not None

    def get_height(self, x, y):
        return self.map.get_height(self, x, y)

    def change_height(self, x, y, val):
        self.map.change_height(self, x, y, val)

    def get_ex_pos(self, layer):
        return self.get_layer(layer).get_ex_pos()

    def get_tile_type(self, layer, x, y):
        return self.get_layer(layer).get_tile_type(x, y)

    def out_of_bounds(self, x, y):
        return not (0 <= x < self.size and 0 <= y < self.size)
