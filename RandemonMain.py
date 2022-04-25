from mapClasses.Map import Map
from render import Render

import time


def main():
    t = time.time()
    my_map = Map(8, 8, 50, max_buildings=16, height_map=False)
    rt = time.time()
    r = Render(my_map)
    print("Rendertime=" + str(time.time() - rt))
    print("Generationtime=" + str(time.time() - t))
    r.show()
    r.save_prompt(my_map)


if __name__ == "__main__":
    main()
