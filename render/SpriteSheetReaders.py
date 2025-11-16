from enum import Enum

from render.SpriteSheetReader import SpriteSheetReader


class SpriteSheetReaders(Enum):
    PATH = SpriteSheetReader("PATH", "path.png", 5, 1545)
    WATER = SpriteSheetReader("WATER", "water.png", 5, 1755)
    NATURE = SpriteSheetReader("NATURE", "nature.png", 6, 1695)
    HILLS = SpriteSheetReader("HILLS", "hills.png", 10, 145)
    ROAD = SpriteSheetReader("ROAD", "road.png", 6, 1743)
    BUILDINGS = SpriteSheetReader("BUILDINGS", "houses.png", 27, 195)
    FENCE = SpriteSheetReader("FENCE", "fences.png", 3, 109)
    POKEMON = SpriteSheetReader("POKEMON", "pokemon.png", 0, 0)
    DECO = SpriteSheetReader("DECO", "decoration.png", 12, 1)
    RAIN = SpriteSheetReader("RAIN", "rain.png", 0, 0)
    HEIGHTS = SpriteSheetReader("HEIGHTS", "heights.png", 0, 0)
    TNF = SpriteSheetReader("TNF", "tnf.png", 0, 0)
