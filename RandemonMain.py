from mapClasses.Map import Map
from render import Render
from colorama import Fore
from colorama import Style

import time
import parser as inputs


def main():
    parser = inputs.make_parser()
    args = parser.parse_args()
    t = time.time()
    my_map: Map = Map(
        args.chunks_horizontal,
        args.chunks_vertical,
        args.chunk_size,
        max_buildings=args.max_buildings,
        height_map=args.height_map_opt,
        island=not args.mainland_opt,
        themed_towns=args.themed_towns_opt
    )
    r = Render(my_map)
    print(Fore.LIGHTBLACK_EX + "Total generation time={}{}".format(str(time.time() - t), "s") + Style.RESET_ALL)
    if not args.no_show_opt:
        r.show()
    if args.save_opt:
        r.save(str(my_map.seed))
    else:
        r.save_prompt(my_map.seed)


if __name__ == "__main__":
    main()
