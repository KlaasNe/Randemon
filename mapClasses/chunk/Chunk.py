from mapClasses.layer import *


class Chunk:

    def __init__(self, size):
        self.size = size
        self.layers = dict()
        for layer in Layers:
            self.layers[layer.name] = layer.value

    def get_layer(self, layer):
        return self.layers[layer]

    def has_tile_at(self, x, y):
        for layer in self.layers:
            if layer.get_tile_img(self, x, y) is not None:
                return False
        return True
