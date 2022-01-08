from mapClasses.Map import Map
from render import Render

import time


def main():
    t = time.time()
    my_map = Map(1, 1, 50)
    r = Render(my_map)
    print("Rendertime=", time.time() - t)
    r.show()


if __name__ == "__main__":
    main()
