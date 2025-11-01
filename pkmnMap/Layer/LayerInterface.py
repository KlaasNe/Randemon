from typing import Optional, Iterator


class LayerInterface:

    def remove_tile(self, x: int, y: int) -> None:
        pass

    def has_tile_at(self, x: int, y: int) -> bool:
        pass

    def get_ex_pos(self) -> Iterator[tuple[int, int]]:
        pass

    def has_tiles_in_area(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        pass

    def get_tile_type(self, x: int, y: int) -> Optional[str]:
        pass

    def clear(self) -> None:
        pass

    def to_json(self):
        pass
