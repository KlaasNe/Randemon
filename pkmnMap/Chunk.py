from typing import Iterator, Optional

from buildings.Building import Building
from pkmnMap import HeightMap
from pkmnMap.Layer import Layer
from pkmnMap.Layer.LayersFactory import LayersFactory
from pkmnMap.tiles.Tile import Tile

MAX_HEIGHT = 5


class Chunk:

    def __init__(self, height_map: HeightMap, size: int, chunk_x: int, chunk_y: int, off_x: int, off_y: int, max_buildings: int) -> None:
        self.height_map: HeightMap = height_map
        self.size: int = size
        self.off_x: int = off_x
        self.off_y: int = off_y
        self.chunk_x: int = chunk_x
        self.chunk_y: int = chunk_y
        self.layers: dict[str, Layer] = LayersFactory.create_layers()
        self.buildings: list[Building] = []
        self.has_town: bool = False
        self.can_have_town: bool = True
        self.path_tiles: set[tuple[int, int]] = set()
        self.route: list[bool] = [False, False, False, False]  # [N, E, S, W] route connection
        self.hill_tiles: set[tuple[int, int]] = set()
        self.max_buildings: int = max_buildings

    def __getitem__(self, layer: str) -> Layer:
        return self.layers[layer]

    def __repr__(self):
        return f"Chunk ({self.chunk_x}, {self.chunk_y})"

    def round_and_copy(self, input_array):
        # Use list comprehensions for a more concise and efficient solution
        rounded_matrix = [[round(value) for value in inner_array] for inner_array in input_array]
        return rounded_matrix

    def get_layers(self) -> Iterator[Layer]:
        return self.layers.values().__iter__()

    def clear_layer(self, layer: str) -> None:
        self.layers[layer].clear()

    def get_tile(self, layer: str, x: int, y: int) -> Optional[Tile]:
        return self[layer][(x, y)]

    def set_tile(self, layer: str, x: int, y: int, tile: Tile) -> None:
        self[layer][(x, y)] = tile

    def remove_tile(self, layer: str, x: int, y: int) -> None:
        self[layer].remove_tile(x, y)

    def has_tile_at(self, x: int, y: int) -> bool:
        for layer in self.layers.keys():
            if self.has_tile_in_layer_at(layer, x, y):
                return True
        return False

    def has_tile_in_layer_at(self, layer: str, x: int, y: int) -> bool:
        return self[layer].has_tile_at(x, y)

    def height_map_pos(self, x: int, y: int) -> tuple[int, int] | None:
        """
        Find the position of a tiles in the global height map based on its Chunk.
        :rtype: tuple[int, int]
        :param x: position of the tiles
        :param y: position of the tiles
        :return: position of a tiles in the height map based on it's Chunk
        """
        try:
            return self.chunk_x * self.size + x, self.chunk_y * self.size + y
        except TypeError as e:
            print(e, self.chunk_x, self.chunk_y, x, y)

    def get_height_exact(self, x: int, y: int) -> float:
        hmx, hmy = self.height_map_pos(x, y)
        try:
            return self.height_map[hmy][hmx]
        except IndexError:
            return 0

    def get_height(self, x: int, y: int) -> int:
        hmx, hmy = self.height_map_pos(x, y)
        try:
            return round(self.height_map[hmy][hmx])
        except IndexError:
            return 0

    def get_tile_type(self, layer: str, x: int, y: int) -> Optional[str]:
        return self[layer].get_tile_type(x, y)

    def out_of_bounds(self, x: int, y: int) -> bool:
        return not (0 <= x < self.size and 0 <= y < self.size)

    def to_json(self):
        return {
            "Layer": [layer.to_json() for layer in self.get_layers()]
        }
