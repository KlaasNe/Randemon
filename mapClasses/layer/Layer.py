from typing import Optional, Iterator

from mapClasses.tile import Tile


class Layer:

    def __init__(self) -> None:
        self.tiles: dict[tuple[int, int], Tile] = dict()

    def __getitem__(self, pos: tuple[int, int]) -> Tile:
        return self.tiles.get(pos, None)

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        return self.tiles.get((x, y), None)

    def get_items(self):
        for item in self.tiles.items():
            yield item

    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        self.tiles[(x, y)] = tile

    def remove_tile(self, x: int, y: int) -> None:
        self.tiles.pop((x, y))

    def get_ex_pos(self) -> Iterator[tuple[int, int]]:
        return self.tiles.keys().__iter__()

    def has_tiles_in_area(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                if self.get_tile(x, y) is not None:
                    return True
        return False

    def get_tile_type(self, x: int, y: int) -> Optional[str]:
        tile: Tile = self.get_tile(x, y)
        return None if tile is None else tile.type

    def clear(self) -> None:
        self.tiles.clear()
