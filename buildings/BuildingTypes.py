from enum import Enum

from buildings.BuildingType import BuildingType


class BuildingTypes(Enum):
    POKECENTER = BuildingType("pokecenter", (14, 0), (5, 5), (2, 4))
    POKEMART = BuildingType("pokemart", (0, 0), (4, 4), (1, 3))
    GYM = BuildingType("gym", (19, 23), (6, 5), (3, 4))
    POWERPLANT = BuildingType("powerplant", (16, 34), (11, 7), (6, 6))
    H0 = BuildingType("h0", (4, 0), (5, 4), (1, 3))
    H1 = BuildingType("h1", (9, 0), (5, 4), (1, 3))
    H2 = BuildingType("h2", (0, 4), (4, 5), (1, 4))
    H3 = BuildingType("h3", (4, 4), (5, 4), (1, 3))
    H4 = BuildingType("h4", (9, 4), (5, 4), (1, 3))
    H5 = BuildingType("h5", (0, 9), (4, 4), (1, 3))
    H6 = BuildingType("h6", (4, 9), (5, 4), (1, 3))
    H7 = BuildingType("h7", (9, 9), (5, 4), (1, 3))
    H8 = BuildingType("h8", (0, 13), (4, 5), (1, 4))
    H9 = BuildingType("h9", (4, 13), (5, 4), (1, 3))
    H10 = BuildingType("h10", (9, 13), (5, 3), (1, 2))
    H11 = BuildingType("h11", (0, 18), (4, 5), (1, 4))
    H12 = BuildingType("h12", (4, 17), (5, 4), (1, 3))
    H13 = BuildingType("h13", (9, 16), (5, 5), (1, 4))
    H14 = BuildingType("h14", (0, 23), (4, 7), (1, 6))
    H15 = BuildingType("h15", (14, 10), (5, 5), (3, 4))
    H16 = BuildingType("h16", (14, 15), (5, 5), (3, 4))
    H17 = BuildingType("h17", (14, 25), (5, 5), (3, 4))
    H18 = BuildingType("h18", (13, 30), (6, 4), (3, 3))
    H19 = BuildingType("h19", (19, 0), (7, 5), (1, 4))
    H20 = BuildingType("h20", (19, 12), (7, 6), (1, 5))
    H21 = BuildingType("h21", (19, 28), (7, 4), (1, 3))
