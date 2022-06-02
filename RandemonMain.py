from mapClasses.Map import Map
from render import Render
from colorama import Fore
from colorama import Style

import time


def main():
    t = time.time()
    my_map = Map(8, 8, 50, max_buildings=16, height_map=False)
    r = Render(my_map)
    print(Fore.LIGHTBLACK_EX + "Total generationtime=" + str(time.time() - t) + Style.RESET_ALL)
    r.show()
    r.save_prompt(my_map)


if __name__ == "__main__":
    main()
