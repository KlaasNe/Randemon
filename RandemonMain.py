from mapClasses.Map import Map
from render import Render
from colorama import Fore
from colorama import Style

import time


def main():
    t = time.time()
    my_map = Map(4, 4, 50, max_buildings=16, height_map=False, island=True, seed=5909710306400228897)
    r = Render(my_map)
    print(Fore.LIGHTBLACK_EX + "Total generationtime={}{}".format(str(time.time() - t), "s") + Style.RESET_ALL)
    r.show()
    r.save_prompt(my_map)


if __name__ == "__main__":
    main()
