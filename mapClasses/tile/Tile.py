import json


class Tile:

    def __init__(self, reader_name: str, x: int, y: int, mirror: bool = False) -> None:
        self.type: str = reader_name
        self.x: int = x
        self.y: int = y
        self.mirror: bool = mirror

    def __eq__(self, other) -> bool:
        return other is not None \
               and self.x == other.x \
               and self.y == other.y \
               and self.type == other.type \
               and self.mirror == other.mirror

    def __str__(self) -> str:
        return "Tile: " + ', '.join("%s=%s" % item for item in vars(self).items())

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.type))

    def to_json(self):
        return {
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "mirror": self.mirror
        }
