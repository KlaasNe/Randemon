import os

from PIL import ImageOps, Image

from randemonPy.mapClasses import Tile

TILE_SIZE = 16
TILE_SHEET_DIRECTORY = os.path.join("randemonPy", "render", "tileSheets")


class SpriteSheetReader:

    def __init__(self, name: str, path: str) -> None:
        self.name: str = name
        self.tiles: dict[int, bytes] = dict()
        with Image.open(os.path.join(TILE_SHEET_DIRECTORY, path)).convert("RGBA") as tile_sheet:
            tile_sheet.load()
            self._init_tiles(tile_sheet)

    def _init_tiles(self, tile_sheet) -> None:
        width, height = tile_sheet.size
        for y in range(height // TILE_SIZE):
            for x in range(width // TILE_SIZE):
                tx, ty = x * TILE_SIZE, y * TILE_SIZE
                self.tiles[hash(Tile(self.name, x, y))] = tile_sheet.crop((tx, ty, tx + TILE_SIZE, ty + TILE_SIZE))

    def get_tile(self, tile: Tile) -> Image:
        img = self.tiles[hash(tile)]
        return ImageOps.mirror(img) if tile.mirror else img
