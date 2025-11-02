import os
from datetime import datetime

from colorama import Fore
from colorama import Style

import parser as inputs
from pkmnMap.PkmnMapFactory import PkmnMapFactory
from render import Render


def main(**kwargs):
    parser = inputs.make_parser()
    args = parser.parse_args()
    if not os.path.isdir(args.save_directory) and not args.save_directory == "saved_images":
        print(Fore.RED + "[Error] The requested directory doesn't exist" + Style.RESET_ALL)
        exit(-1)
    pkmn_map = PkmnMapFactory.create_pkmn_map(
        args.chunks_horizontal,
        args.chunks_vertical,
        args.chunk_size,
        max_buildings=args.max_buildings,
        make_height_map=args.height_map_opt,
        island=not args.mainland_opt,
        themed_towns=args.themed_towns_opt,
        seed=args.seed,
        terrain_chaos=args.terrain_chaos,
        max_height=args.max_height,
        town_map=args.town_map,
    )

    with open("map.json", "w+") as file:
        file.write(pkmn_map.to_json())
    r = Render()
    r.render(pkmn_map, args.town_map)

    if not args.no_show_opt:
        r.show()
    if args.save_opt:
        r.save("{} {}".format(datetime.now().strftime("%G-%m-%d %H-%M-%S"), str(pkmn_map.seed)),
               directory=args.save_directory)
    else:
        r.save_prompt(pkmn_map.seed, directory=args.save_directory)


if __name__ == "__main__":
    main()
