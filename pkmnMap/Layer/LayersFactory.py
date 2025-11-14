from enum import Enum, auto

from pkmnMap.Layer import Layer


class Layers(Enum):
    GROUND0 = auto()
    HILLS = auto()
    FENCE = auto()
    BUILDINGS = auto()
    GROUND1 = auto()
    GROUND2 = auto()
    HEIGHTMAP = auto()


class LayersFactory:

    @staticmethod
    def create_layers() -> dict[str, Layer]:
        return {layer.name: Layer(layer.name) for layer in Layers}
