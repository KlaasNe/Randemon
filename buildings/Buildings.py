from enum import Enum

from buildings.Building import Building


class Buildings(Enum):
    POKECENTER = Building("pokecenter", (14, 0), (5, 5), (2, 4))
    POKEMART = Building("pokemart", (0, 0), (4, 4), (2, 3))
    GYM = Building("gym", (19, 23), (6, 5), (3, 5))
    POWERPLANT = Building("powerplant", (16, 34), (11, 7), (6, 8))
    H0 = Building("h0", (4, 0), (5, 4), (1, 3))
    H1 = Building("h1", (9, 0), (5, 4), (1, 3))
    H2 = Building("h2", (0, 4), (4, 5), (1, 3))
    H3 = Building("h3", (4, 4), (5, 4), (1, 3))
    H4 = Building("h4", (9, 4), (5, 4), (1, 3))
    H5 = Building("h5", (0, 9), (4, 4), (1, 3))
    H6 = Building("h6", (4, 9), (5, 4), (1, 3))
    H7 = Building("h7", (9, 9), (5, 4), (1, 3))
    H8 = Building("h8", (0, 13), (4, 5), (1, 3))
    H9 = Building("h9", (4, 13), (5, 4), (1, 3))
    H10 = Building("h10", (9, 13), (5, 3), (1, 3))
    H11 = Building("h11", (0, 18), (4, 5), (1, 3))
    H12 = Building("h12", (4, 17), (5, 4), (1, 3))
    H13 = Building("h13", (9, 16), (5, 5), (1, 3))
    H14 = Building("h14", (0, 23), (4, 7), (1, 3))
    H15 = Building("h15", (14, 10), (5, 5), (3, 3))
    H16 = Building("h16", (14, 15), (5, 5), (3, 3))
    H17 = Building("h17", (14, 25), (5, 5), (3, 3))
    H18 = Building("h18", (13, 30), (6, 4), (3, 3))
    H19 = Building("h19", (19, 0), (7, 5), (1, 3))
    H20 = Building("h20", (19, 12), (7, 6), (1, 3))
    H21 = Building("h21", (19, 28), (7, 4), (1, 3))
