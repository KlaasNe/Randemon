from mapClasses.layer import *


class Chunk:

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        for layer in Layers:
            self.layers = dict()[layer] = layer.value

    def has_tile_at(self, x, y):
        for layer in self.layers:
            if layer.get_tile(self, x, y) is not None:
                return False
        return True
