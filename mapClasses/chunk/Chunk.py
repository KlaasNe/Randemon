from typing import Iterator

from generators.heightMapGenerator import get_height
from mapClasses.tile import Tile
from mapClasses.layer import *

MAX_HEIGHT = 5


class Chunk:

    def __init__(self, height_map: list[list[int]], size: int, chunk_x: int, chunk_y: int, off_x: int, off_y: int) -> None:
        self.height_map = height_map
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

    def __getitem__(self, layer: str) -> Layer:
        return self.layers[layer]

    def get_layer(self, layer: str) -> Layer:
        return self.layers[layer]

    def get_layers(self) -> Iterator[Layer]:
        return self.layers.values().__iter__()

    def clear_layer(self, layer: str) -> None:
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

    def height_map_pos(self, x: int, y: int) -> tuple[int, int]:
        return self.chunk_x * self.size + x, self.chunk_y * self.size + y

    def get_height(self, x: int, y: int) -> int:
        hmx, hmy = self.height_map_pos(x, y)
        try:
            return self.height_map[hmy][hmx]
        except IndexError:
            return 0

    def change_height(self, x: int, y: int, val: int) -> None:
        hmx, hmy = self.height_map_pos(x, y)
        self.height_map[hmy][hmx] += val

    def get_tile_type(self, layer: str, x: int, y: int) -> Optional[str]:
        return self.get_layer(layer).get_tile_type(x, y)

    def out_of_bounds(self, x: int, y: int) -> bool:
        return not (0 <= x < self.size and 0 <= y < self.size)
