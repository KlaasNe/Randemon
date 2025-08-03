from typing import Optional

from mapStructure.chunks.Chunk import Chunk


class PkmnMapInterface:

    def create(self) -> None:
        pass

    def process_chunk(self, coords) -> None:
        pass

    def get_chunk(self, x, y) -> Optional[Chunk]:
        pass

    def in_bounds(self, x: int, y: int) -> bool:
        pass

    def parse_to_coordinate_on_map(self, c: Chunk, x: int, y: int) -> tuple[int, int]:
        pass

    def parse_to_coordinate_in_chunk(self, x: int, y: int) -> tuple[Chunk, int, int]:
        pass

    def get_height_map_pos(self, x: int, y: int) -> int:
        pass

    def get_height(self, c: Chunk, x: int, y: int) -> int:
        pass

    def change_height(self, c: Chunk, x: int, y: int, val: int) -> None:
        pass

    def to_json(self) -> str:
        pass