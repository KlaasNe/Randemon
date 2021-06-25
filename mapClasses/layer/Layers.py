from .Layer import Layer
from enum import Enum


class Layers(Enum):
    GROUND0 = Layer()
    HILLS = Layer()
    BUILDINGS = Layer()
    GROUND1 = Layer()
    GROUND2 = Layer()
