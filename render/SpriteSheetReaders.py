import os
from enum import Enum

from PIL import Image

from render.SpriteSheetReader import SpriteSheetReader

TILE_SHEET_DIRECTORY = os.path.join("render", "tileSheets")


class SpriteSheetReaders(Enum):
    PATH = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "path.png")))
    WATER = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "water.png")))
    NATURE = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "nature.png")))
    HILLS = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "hills.png")))
    ROAD = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "road.png")))
    BUILDINGS = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "houses.png")))
    FENCE = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "fences.png")))
    POKEMON = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "pokemon.png")))
    DECO = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "decoration.png")))
    RAIN = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "rain.png")))
    TNF = SpriteSheetReader(Image.open(os.path.join(TILE_SHEET_DIRECTORY, "tnf.png")))
