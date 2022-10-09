from mapClasses.Map import Map
from render import Render
from colorama import Fore
from colorama import Style

import time


def main():
    t = time.time()
    my_map: Map = Map(4, 4, 50, max_buildings=16, height_map=False, island=True, themed_towns=True)
    r = Render(my_map)
    print(Fore.LIGHTBLACK_EX + "Total generation time={}{}".format(str(time.time() - t), "s") + Style.RESET_ALL)
    r.show()
    r.save_prompt(my_map.seed)


if __name__ == "__main__":
    main()
