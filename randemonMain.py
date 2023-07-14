import io
import os
import io
import random
import time
from datetime import datetime
from sys import maxsize

from colorama import Fore
from colorama import Style
from starlette.responses import Response

import parser as inputs
from mapClasses import Map
from render import Render
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RandemonAPI"
)

origins = [
    "http://localhost:8000",
    "http://localhost:63342",
    "http://localhost:63343",
    "https://klaasne.github.io"
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
            kwargs.get("nb_chunks_horizontal"),
            kwargs.get("nb_chunks_vertical"),
            kwargs.get("chunk_size"),
            max_buildings=kwargs.get("max_buildings"),
            make_height_map=kwargs.get("height_map"),
            island=kwargs.get("island"),
            themed_towns=kwargs.get("themed_towns"),
            seed=kwargs.get("seed"),
            terrain_chaos=4,
            max_height=6,
            town_map=kwargs.get("town_map"),
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
            max_height=args.max_height,
            town_map=args.town_map,
        )
    my_map.create()
    r = Render()
    r.render(my_map)
    if api_request:
        return r.visual
    else:
        print(Fore.LIGHTBLACK_EX + f"Total generation time={str(time.time() - t)}s" + Style.RESET_ALL)
        if not args.no_show_opt:
            r.show()
        if args.save_opt:
            r.save("{} {}".format(datetime.now().strftime("%G-%m-%d %H-%M-%S"), str(my_map.seed)),
                   directory=args.save_directory)
        else:
            r.save_prompt(my_map.seed, directory=args.save_directory)


@app.get("/")
async def root(seed: int = None,
               height_map: bool = False,
               island: bool = True,
               nb_chunks_horizontal: int = 4,
               nb_chunks_vertical: int = 4,
               chunk_size: int = 50,
               max_buildings: int = 16,
               themed_towns: bool = True,
               town_map: bool = True):
    if seed is None:
        seed = random.randint(0, maxsize)
    img = main(
        api_request=True,
        seed=seed,
        height_map=height_map,
        island=island,
        nb_chunks_horizontal=nb_chunks_horizontal,
        nb_chunks_vertical=nb_chunks_vertical,
        chunk_size=chunk_size,
        max_buildings=max_buildings,
        themed_towns=themed_towns
    )
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return Response(content=img_io.getvalue(), media_type="image/png")


if __name__ == "__main__":
    main()
