from mapClasses.layer import *
from buildings import Building

MAX_HEIGHT = 5


class Chunk:

    def __init__(self, height_map: list[list[int]], size: int, chunk_x: int, chunk_y: int, off_x: int, off_y: int) -> None:
        self.height_map: list[list[int]] = height_map
        self.size: int = size
        self.off_x: int = off_x
        self.off_y: int = off_y
        self.chunk_x: int = chunk_x
        self.chunk_y: int = chunk_y
        self.layers: dict[str, Layer] = dict()
        for layer in Layers:
            self.layers[layer.name] = Layer()
        self.buildings: list[Building] = []
        self.has_town: bool = False
        self.can_have_town: bool = True
        self.path_tiles: set[tuple[int, int]] = set()
        self.route = None

    def __getitem__(self, layer: str) -> Layer:
        return self.layers[layer]

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

    def height_map_pos(self, x: int, y: int) -> tuple[int, int]:
        """
        Find the position of a tile in the global height map based on it's chunk.
        :rtype: tuple[int, int]
        :param x: position of the tile
        :param y: position of the tile
        :return: position of a tile in the height map based on it's chunk
        """
        try:
            return self.chunk_x * self.size + x, self.chunk_y * self.size + y
        except TypeError as e:
            print(self.chunk_x, self.chunk_y, x, y)

    def get_height_exact(self, x: int, y: int) -> int:
        hmx, hmy = self.height_map_pos(x, y)
        try:
            return self.height_map[hmy][hmx]
        except IndexError:
            return 0

    def get_height(self, x: int, y: int) -> int:
        return round(self.get_height_exact(x, y))

    def change_height(self, x: int, y: int, val: int) -> None:
        hmx, hmy = self.height_map_pos(x, y)
        self.height_map[hmy][hmx] += val
        self.height_map[hmy][hmx] = max(self.height_map[hmy][hmx], .16)  # TODO hardcoded based on .15 dark water

    def get_tile_type(self, layer: str, x: int, y: int) -> Optional[str]:
        return self[layer].get_tile_type(x, y)

    def out_of_bounds(self, x: int, y: int) -> bool:
        return not (0 <= x < self.size and 0 <= y < self.size)
