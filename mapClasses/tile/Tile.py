class Tile:

    def __init__(self, reader_name: str, x: int, y: int, mirror: bool = False) -> None:
        self.reader_name = reader_name
        self.x = x
        self.y = y
        self.mirror = mirror

    def __eq__(self, other) -> bool:
        return other is not None \
               and self.x == other.x \
               and self.y == other.y \
               and self.reader_name == other.reader_name \
               and self.mirror == other.mirror

    def __str__(self) -> str:
        return "Tile: " + ', '.join("%s=%s" % item for item in vars(self).items())

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.reader_name, self.mirror))

    def get_type(self) -> str:
        return self.reader_name
