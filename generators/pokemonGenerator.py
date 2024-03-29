from random import random, randint
from generators.pathGenerator import get_path_type
from colorama import Fore
from colorama import Style

# Spawns pokémon on the map most in the pmap.ground_layer
# Returns true if all existing pokémon are present on the map
from mapClasses.tile import Tile

pokemon_data = {
    "diglett": {"pos": (0, 0), "size": (1, 1), "odds": 0.001},
    "lapras": {"pos": (1, 0), "size": (1, 2), "odds": 0.001},
    "gyarados": {"pos": (2, 0), "size": (2, 2), "odds": 0.0005},
    "snorlax": {"pos": (4, 0), "size": (2, 2), "odds": 0.035},
    "exeggutor": {"pos": (6, 0), "size": (1, 2), "odds": 0.0025},
    "togetic": {"pos": (7, 0), "size": (1, 2), "odds": 0.0001},
    "seel": {"pos": (8, 0), "size": (1, 1), "odds": 0.0025}
}

SHINY_PROBABILITY = 0.001


# May the odds be ever in your favour.
def good_odds(odds):
    return odds > random()


def coinflip():
    return randint(0, 1) == 0


def spawn_pokemons(chunk, shiny_detector=True):
    def is_enough_water_space(x1, y1, x2, y2):
        for check_y in range(y1, y2 + 1):
            for check_x in range(x1, x2 + 1):
                if "WATER" != chunk.get_tile_type("GROUND0", check_x, check_y) or "POKEMON" == chunk.get_tile_type(
                        "GROUND0", check_x, check_y):
                    return False
        return True

    def spawn_lapras(odds):
        lapras = False
        for y in range(chunk.size):
            for x in range(chunk.size):
                if good_odds(odds) and is_enough_water_space(x - 1, y - 1, x + 1, y + 2):
                    if random() < SHINY_PROBABILITY:
                        shiny = 2
                        if shiny_detector:
                            print(Fore.LIGHTMAGENTA_EX + f"shiny lapras at ({x}, {y})" + Style.RESET_ALL)
                    else:
                        shiny = 0
                    mirror = coinflip()
                    chunk.set_tile("GROUND2", x, y, Tile("POKEMON", 1, shiny, mirror))
                    chunk.set_tile("GROUND2", x, y + 1, Tile("POKEMON", 1, 1 + shiny, mirror))
                lapras = True
        return lapras

    def spawn_gyarados(odds):
        gyarados = False
        for y in range(0, chunk.size):
            for x in range(0, chunk.size):
                if good_odds(odds) and is_enough_water_space(x - 1, y - 1, x + 2, y + 2):
                    if random() < SHINY_PROBABILITY:
                        shiny = 2
                        if shiny_detector:
                            print(Fore.LIGHTMAGENTA_EX + f"shiny gyarados at ({x}, {y})" + Style.RESET_ALL)
                    else:
                        shiny = 0
                    mirror = coinflip()
                    if mirror:
                        for gyarados_tile in range(4):
                            chunk.set_tile("GROUND2", x + gyarados_tile % 2, y + gyarados_tile // 2,
                                           Tile("POKEMON", 2 + 1 - gyarados_tile % 2, gyarados_tile // 2 + shiny,
                                                mirror))
                    else:
                        for gyarados_tile in range(4):
                            chunk.set_tile("GROUND2", x + gyarados_tile % 2, y + gyarados_tile // 2,
                                           Tile("POKEMON", 2 + gyarados_tile % 2, gyarados_tile // 2 + shiny))
                    gyarados = True
        return gyarados

    def spawn_diglett(odds):
        diglett = False
        for y in range(0, chunk.size):
            for x in range(0, chunk.size):
                if good_odds(odds) and not chunk.has_tile_in_layer_at("GROUND0", x,
                                                                      y) and not chunk.has_tile_in_layer_at("BUILDINGS",
                                                                                                            x, y) and \
                        chunk["HILLS"][(x, y)] == None:
                    if random() < SHINY_PROBABILITY:
                        shiny = 2
                        if shiny_detector:
                            print(Fore.LIGHTMAGENTA_EX + f"shiny diglett at ({x}, {y})" + Style.RESET_ALL)
                    else:
                        shiny = 0
                    mirror = coinflip()
                    chunk.set_tile("GROUND2", x, y, Tile("POKEMON", 0, shiny, mirror))
                    diglett = True
        return diglett

    def spawn_snorlax(odds):
        def check_bridge_space(x1, y1, x2, y2):
            for check_y in range(y1, y2 + 1):
                for check_x in range(x1, x2 + 1):
                    if chunk.get_tile_type("GROUND0", check_x, check_y) != "ROAD":
                        return False
                    if chunk.get_tile_type("GROUND2", check_x, check_y) == "POKEMON":
                        return False
            return True

        snorlax = False
        shiny = 0
        for y in range(0, chunk.size):
            for x in range(0, chunk.size):
                if good_odds(odds) and "ROAD" == chunk.get_tile_type("GROUND0", x, y) and check_bridge_space(x, y,
                                                                                                             x + 1,
                                                                                                             y + 1):
                    if random() < SHINY_PROBABILITY:
                        shiny = 2
                        if shiny_detector:
                            print(Fore.LIGHTMAGENTA_EX + f"shiny snorlax at ({x}, {y})" + Style.RESET_ALL)
                    else:
                        shiny = 0
                    for snorlax_tile in range(4):
                        chunk.set_tile("GROUND2", x + snorlax_tile % 2, y + snorlax_tile // 2,
                                       Tile("GROUND2", 4 + snorlax_tile % 2, snorlax_tile // 2 + shiny))
                    snorlax = True
        return snorlax

    def spawn_exceguttor(odds):
        exceguttor = False
        for (x, y), tile in chunk["GROUND0"]:
            if good_odds(odds) and get_path_type(chunk["GROUND0"], x, y) == 3:
                if random() < SHINY_PROBABILITY:
                    shiny = 2
                    if shiny_detector:
                        print(Fore.LIGHTMAGENTA_EX + f"shiny exceguttor at ({x}, {y})" + Style.RESET_ALL)
                else:
                    shiny = 0
                mirror = coinflip()
                chunk["GROUND2"][(x, y)] = Tile("POKEMON", 6, 1 + shiny, mirror)
                chunk["GROUND2"][(x, y - 1)] = Tile("POKEMON", 6, shiny, mirror)
            exceguttor = True
        return exceguttor

    def spawn_togetic(odds):
        togetic = False
        for y in range(0, chunk.height):
            for x in range(0, chunk.width):
                if good_odds(odds):
                    if random() < SHINY_PROBABILITY:
                        shiny = 2
                        if shiny_detector:
                            print(Fore.LIGHTMAGENTA_EX + f"shiny togetic at ({x}, {y})" + Style.RESET_ALL)
                    else:
                        shiny = 0
                    mirror = coinflip()
                    chunk.decoration.set_tile((x, y), ("po", 7, shiny, mirror))
                    chunk.decoration.set_tile((x, y + 1), ("po", 7, 1 + shiny, mirror))
                    togetic = True
        return togetic

    def spawn_cleffa(odds: float) -> bool:
        cleffa = False
        for (x, y), tile in chunk["HILLS"]:
            if (tile == Tile("HILLS", 0, 4) or tile == Tile("HILLS", 5, 4)) and good_odds(odds):
                if random() < SHINY_PROBABILITY:
                    shiny = 2
                    if shiny_detector:
                        print(Fore.LIGHTMAGENTA_EX + f"shiny cleffa at ({x}, {y})" + Style.RESET_ALL)
                else:
                    shiny = 0
                mirror = coinflip()
                chunk["GROUND2"][(x, y + 1)] = Tile("POKEMON", 9, shiny, mirror)
                cleffa = True
        return cleffa

    lapras = spawn_lapras(0.00005)
    gyarados = spawn_gyarados(0.00005)
    diglett = spawn_diglett(0.0005)
    snorlax = spawn_snorlax(0.025)
    exceguttor = spawn_exceguttor(0.0005)
    # togetic = spawn_togetic(0.0001)
    cleffa = spawn_cleffa(0.2)

    # return lapras and diglett and snorlax and exceguttor and gyarados and togetic
