from generators.heightMapGenerator import generate_height_map
from mapClasses.layer import *


class Chunk:

    def __init__(self, size, off_x, off_y):
        self.size = size
        self.layers = dict()
        for layer in Layers:
            self.layers[layer.name] = layer.value
        self.height_map = generate_height_map(self.size, 4, off_x, off_y)

    def get_layer(self, layer):
        return self.layers[layer]

    def has_tile_at(self, x, y):
        for layer in self.layers.values():
            if layer.get_tile(x, y) is not None:
                return True
        return False
