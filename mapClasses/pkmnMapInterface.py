from typing import Optional

from mapClasses.chunks import Chunk


class PkmnMapInterface:

    def create(self):
        pass

    def process_chunk(self, coords):
        pass

    def get_chunk(self, x, y) -> Optional[Chunk]:
        pass

    def in_bounds(self, x: int, y: int) -> bool:
        pass