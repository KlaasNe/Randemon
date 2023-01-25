from enum import Enum
from random import choices

from randemonPy.buildings.BuildingType import BuildingType
from randemonPy.buildings.BuildingTheme import BuildingTheme


class BuildingTypes(Enum):
    POKECENTER = BuildingType("pokecenter", (14, 0), (5, 5), (2, 4))
    POKEMART = BuildingType("pokemart", (0, 0), (4, 4), (1, 3))
    GYM = BuildingType("gym", (19, 23), (6, 5), (3, 4))
    POWERPLANT = BuildingType("powerplant", (16, 34), (11, 7), (6, 6))
    H0 = BuildingType("h0", (4, 0), (5, 4), (1, 3))  # basic green roof chimney
    H1 = BuildingType("h1", (9, 0), (5, 4), (1, 3))  # basic black roof
    H2 = BuildingType("h2", (0, 4), (4, 5), (1, 4))  # small cube yellow
    H3 = BuildingType("h3", (4, 4), (5, 4), (1, 3))  # basic purple roof
    H4 = BuildingType("h4", (9, 4), (5, 4), (1, 3))  # cube red
    H5 = BuildingType("h5", (0, 9), (4, 4), (1, 3))  # basic orange roof
    H6 = BuildingType("h6", (4, 9), (5, 4), (1, 3))  # basic red roof
    H7 = BuildingType("h7", (9, 9), (5, 4), (1, 3))  # Bill's house
    H8 = BuildingType("h8", (0, 13), (4, 5), (1, 4))  # small green apartments
    H9 = BuildingType("h9", (4, 13), (5, 4), (1, 3))  # cube purple
    H10 = BuildingType("h10", (9, 13), (5, 3), (1, 2))  # blue roof
    H11 = BuildingType("h11", (0, 18), (4, 5), (1, 4))  # yellow house green roof small
    H12 = BuildingType("h12", (4, 17), (5, 4), (1, 3))  # savanna house
    H13 = BuildingType("h13", (9, 16), (5, 5), (1, 4))  # big cube yellow
    H14 = BuildingType("h14", (0, 23), (4, 7), (1, 6))  # bicycle shop
    H15 = BuildingType("h15", (14, 10), (5, 5), (3, 4))  # Pallet town house
    H16 = BuildingType("h16", (14, 15), (5, 5), (3, 4))  # basic green roof chimney and flowers
    H17 = BuildingType("h17", (14, 25), (5, 5), (3, 4))  # yellow house green roof big
    H18 = BuildingType("h18", (13, 30), (6, 4), (3, 3))  # turquoise roof small
    H19 = BuildingType("h19", (19, 0), (7, 5), (1, 4))  # Oak's lab
    H20 = BuildingType("h20", (19, 12), (7, 6), (1, 5))  # Mew's mansion
    H21 = BuildingType("h21", (19, 28), (7, 4), (1, 3))  # turquoise roof big


class BuildingThemes(Enum):

    @staticmethod
    def get_random_theme():
        return choices(list(BuildingThemes))[0]

    PALLET_TOWN = BuildingTheme({BuildingTypes.H15: 0.67, BuildingTypes.H19: 0.33})
    VIRIDIAN_CITY = BuildingTheme({BuildingTypes.H0: 0.5, BuildingTypes.H16: 0.5})
    PEWTER_CITY = BuildingTheme({BuildingTypes.H1: 1})  # has science museum
    CERULEAN_CITY = BuildingTheme({BuildingTypes.H18: 0.4375, BuildingTypes.H21: 0.4375, BuildingTypes.H14: 0.125})
    VERMILION_CITY = BuildingTheme({BuildingTypes.H2: 0.5, BuildingTypes.H13: 0.5})  # has pokémon fanclub
    LAVENDER_TOWN = BuildingTheme({BuildingTypes.H9: 1})  # has pokémon tower
    CELADON_CITY = BuildingTheme({BuildingTypes.H8: 0.9, BuildingTypes.H10: 0.1})  # has big appartments and poké mall
    FUCHSIA_CITY = BuildingTheme({BuildingTypes.H4: 0.8, BuildingTypes.H12: 0.2})
    SAFFRON_CITY = BuildingTheme({BuildingTypes.H11: 0.5, BuildingTypes.H17: 0.5})  # has big business tower
    THREE_ISLAND = BuildingTheme({BuildingTypes.H3: 0.75, BuildingTypes.H6: 0.25})
    FOUR_ISLAND = BuildingTheme({BuildingTypes.H3: 0.75, BuildingTypes.H5: 0.25})

    RED = BuildingTheme({BuildingTypes.H4: 0.34, BuildingTypes.H6: 0.33, BuildingTypes.H15: 0.33})
    YELLOW = BuildingTheme({BuildingTypes.H2: 0.25, BuildingTypes.H5: 0.25, BuildingTypes.H12: 0.25, BuildingTypes.H13: 0.25})
    GREEN = BuildingTheme({BuildingTypes.H0: 0.25, BuildingTypes.H7: 0.25, BuildingTypes.H8: 0.25, BuildingTypes.H16: 0.25})
    BLUE = BuildingTheme({BuildingTypes.H10: 0.25, BuildingTypes.H14: 0.25, BuildingTypes.H18: 0.25, BuildingTypes.H21: 0.25})

    FAV = BuildingTheme({BuildingTypes.H7: 0.3, BuildingTypes.H10: 0.3, BuildingTypes.H15: 0.1, BuildingTypes.H16: 0.3})
