import os
import random
import time
from datetime import datetime
from sys import maxsize

from colorama import Fore
from colorama import Style

import parser as inputs
from mapClasses import Map
from render import Render
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="RandemonAPI"
)

origins = [
    "http://localhost:8000",
    "http://localhost:63343",
    "https://klaasne.github.io/randemonMaps"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main(api_request=False, **kwargs):
    if api_request:
        my_map = Map(
            4,
            4,
            50,
            max_buildings=16,
            make_height_map=False,
            island=True,
            themed_towns=True,
            seed=kwargs.get("seed"),
            terrain_chaos=4,
            max_height=6
        )
    else:
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
    if api_request:
        if not os.path.isdir("temp"):
            os.mkdir("temp")
        r.save("temp", directory="temp")
    else:
        if not args.no_show_opt:
            r.show()
        if args.save_opt:
            r.save("{} {}".format(datetime.now().strftime("%G-%m-%d %H-%M-%S"), str(my_map.seed)),
                   directory=args.save_directory)
        else:
            r.save_prompt(my_map.seed, directory=args.save_directory)


@app.get("/")
async def root(seed: int = None):
    if seed is None:
        seed = random.randint(0, maxsize)
    main(api_request=True, seed=seed)
    print(seed)
    return FileResponse("temp/temp.png")


if __name__ == "__main__":
    main()
