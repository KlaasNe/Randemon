from typing import Iterator

from generators.heightMapGenerator import get_height
from mapClasses.tile import Tile
from mapClasses.layer import *

MAX_HEIGHT = 5


class Chunk:

    def __init__(self, pmap, size: int, chunk_x: int, chunk_y: int, off_x: int, off_y: int) -> None:
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

    def get_layer(self, layer: str) -> Layer:
        return self.layers[layer]

    def clear_layer(self, layer: Layer) -> None:
        self.layers[layer].clear()

    def get_tile(self, layer: str, x: int, y: int) -> Optional[Tile]:
        return self.get_layer(layer).get_tile(x, y)

    def set_tile(self, layer: str, x: int, y: int, tile: Tile) -> None:
        self.get_layer(layer).set_tile(x, y, tile)

    def remove_tile(self, layer: str, x: int, y: int) -> None:
        self.get_layer(layer).remove_tile(x, y)

    def has_tile_at(self, x: int, y: int) -> bool:
        for layer in self.layers.keys():
            if self.has_tile_at_layer(layer, x, y):
                return True
        return False

    def has_tile_at_layer(self, layer: str, x: int, y: int) -> bool:
        return self.get_tile(layer, x, y) is not None

    def get_height(self, x: int, y: int) -> int:
        return self.map.get_height(self, x, y)

    def change_height(self, x: int, y: int, val: int) -> None:
        self.map.change_height(self, x, y, val)

    def get_tile_type(self, layer: str, x: int, y: int) -> Optional[str]:
        return self.get_layer(layer).get_tile_type(x, y)

    def out_of_bounds(self, x: int, y: int) -> bool:
        return not (0 <= x < self.size and 0 <= y < self.size)
