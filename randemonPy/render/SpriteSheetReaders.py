from enum import Enum

from randemonPy.render.SpriteSheetReader import SpriteSheetReader


class SpriteSheetReaders(Enum):
    PATH = SpriteSheetReader("PATH", "path.png")
    WATER = SpriteSheetReader("WATER", "water.png")
    NATURE = SpriteSheetReader("NATURE", "nature.png")
    HILLS = SpriteSheetReader("HILLS", "hills.png")
    ROAD = SpriteSheetReader("ROAD", "road.png")
    BUILDINGS = SpriteSheetReader("BUILDINGS", "houses.png")
    FENCE = SpriteSheetReader("FENCE", "fences.png")
    POKEMON = SpriteSheetReader("POKEMON", "pokemon.png")
    DECO = SpriteSheetReader("DECO", "decoration.png")
    RAIN = SpriteSheetReader("RAIN", "rain.png")
    HEIGHTS = SpriteSheetReader("HEIGHTS", "heights.png")
    TNF = SpriteSheetReader("TNF", "tnf.png")
