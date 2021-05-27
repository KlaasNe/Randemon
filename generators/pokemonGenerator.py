from random import random, randint
from generators.pathGenerator import get_path_type


# Spawns pokemon on the map most in the pmap.ground_layer
# Returns true if all existing pokemon are present on the map
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


def spawn_pokemons(pmap):
    def is_enough_water_space(x1, y1, x2, y2):
        for check_y in range(y1, y2 + 1):
            for check_x in range(x1, x2 + 1):
                if "wa" != pmap.ground.get_tile_type((check_x, check_y)) or "po" == pmap.ground.get_tile_type((check_x, check_y)):
                    return False
        return True

    def spawn_lapras(odds):
        lapras = False
        for y in range(pmap.height):
            for x in range(pmap.width):
                if good_odds(odds) and is_enough_water_space(x - 1, y - 1, x + 1, y + 2):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    mirror = coinflip()
                    pmap.ground.set_tile((x, y), ("po", 1, shiny, mirror))
                    pmap.ground.set_tile((x, y + 1), ("po", 1, 1 + shiny, mirror))
                lapras = True
        return lapras

    def spawn_gyarados(odds):
        gyarados = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if good_odds(odds) and is_enough_water_space(x - 1, y - 1, x + 2, y + 2):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    mirror = coinflip()
                    if mirror:
                        for gyarados_tile in range(4):
                            pmap.ground.set_tile((x + gyarados_tile % 2, y + gyarados_tile // 2), ("po", 2 + 1 - gyarados_tile % 2, gyarados_tile // 2 + shiny, mirror))
                    else:
                        for gyarados_tile in range(4):
                            pmap.ground.set_tile((x + gyarados_tile % 2, y + gyarados_tile // 2), ("po", 2 + gyarados_tile % 2, gyarados_tile // 2 + shiny))
                    gyarados = True
        return gyarados

    def spawn_diglett(odds):
        diglett = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if pmap.tile_heights.get((x, y), -1) <= pmap.highest_path and (x, y) not in pmap.ground.get_ex_pos() and (x, y) not in pmap.buildings.get_ex_pos() and good_odds(odds):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    pmap.ground.set_tile((x, y), ("po", 0, shiny, coinflip()))
                    diglett = True
        return diglett

    def spawn_snorlax(odds):
        def check_bridge_space(x1, y1, x2, y2):
            for check_y in range(y1, y2 + 1):
                for check_x in range(x1, x2 + 1):
                    if "ro" != pmap.ground.get_tile((check_x, check_y)):
                        return False
                    if "po" in pmap.decoration_layer.get((check_x, check_y), ""):
                        return False
            return True

        snorlax = False
        shiny = 0
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if "ro" == pmap.ground.get_tile((x, y)) and good_odds(odds) and check_bridge_space(x, y, x + 1, y + 1):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    for snorlax_tile in range(4):
                        pmap.decoration.set_tile((x + snorlax_tile % 2, y + snorlax_tile // 2), ("po", 4 + snorlax_tile % 2, snorlax_tile // 2 + shiny))
                    snorlax = True
        return snorlax

    def spawn_exceguttor(odds):
        exceguttor = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if good_odds(odds) and get_path_type(pmap.ground, x, y) == 3:
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    mirror = coinflip()
                    pmap.ground2.set_tile((x, y), ("po", 6, 1 + shiny, mirror))
                    pmap.ground2.set_tile((x, y - 1), ("po", 6, shiny, mirror))
                exceguttor = True
        return exceguttor

    def spawn_togetic(odds):
        togetic = False
        for y in range(0, pmap.height):
            for x in range(0, pmap.width):
                if good_odds(odds):
                    shiny = 2 if random() < SHINY_PROBABILITY else 0
                    mirror = coinflip()
                    pmap.decoration.set_tile((x, y), ("po", 7, shiny, mirror))
                    pmap.decoration.set_tile((x, y + 1), ("po", 7, 1 + shiny, mirror))
                    togetic = True
        return togetic

    lapras = spawn_lapras(0.001)
    gyarados = spawn_gyarados(0.001)
    diglett = spawn_diglett(0.0005)
    snorlax = spawn_snorlax(0.025)
    exceguttor = spawn_exceguttor(0.0025)
    togetic = spawn_togetic(0.0001)

    return lapras and diglett and snorlax and exceguttor and gyarados and togetic
