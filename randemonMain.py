import os
import time
from datetime import datetime

from colorama import Fore
from colorama import Style

import parser as inputs
from mapClasses import Map
from render import Render


def main():
    parser = inputs.make_parser()
    args = parser.parse_args()
    if not os.path.isdir(args.save_directory) and not args.save_directory == "saved_images":
        print(Fore.RED + "[Error] The given directory doesn't exist" + Style.RESET_ALL)
        exit(-1)
    t = time.time()
    my_map = Map(
        args.chunks_horizontal,
        args.chunks_vertical,
        args.chunk_size,
        max_buildings=args.max_buildings,
        make_height_map=args.height_map_opt,
        island=not args.mainland_opt,
        themed_towns=args.themed_towns_opt,
        seed=args.seed,
        terrain_chaos=args.terrain_chaos,
        max_height=args.max_height
    )
    my_map.create()
    r = Render()
    r.render(my_map)
    print(Fore.LIGHTBLACK_EX + "Total generation time={}s".format(str(time.time() - t)) + Style.RESET_ALL)
    if not args.no_show_opt:
        r.show()
    if args.save_opt:
        r.save("{} {}".format(datetime.now().strftime("%G-%m-%d %H-%M-%S"), str(my_map.seed)),
               directory=args.save_directory)
    else:
        r.save_prompt(my_map.seed, directory=args.save_directory)
    return r


if __name__ == "__main__":
    main()
