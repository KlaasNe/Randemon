import ctypes
import os
from typing import Union

from PIL import Image

from mapClasses.chunk import Chunk

from colorama import Fore
from colorama import Style
from datetime import datetime

from mapClasses import Map, Tile
from render.SpriteSheetReaders import *
from alive_progress import alive_bar


class Render:
    TILE_SIZE = 16
    TNF = Tile("TNF", 0, 0)

    def __init__(self, map_obj: Map) -> None:
        self.readers = dict()
        for reader in SpriteSheetReaders:
            self.readers[reader.name] = reader.value
        chunk_size = map_obj.chunk_size
        chunk_nb_h, chunk_nb_v = map_obj.chunk_nb_h, map_obj.chunk_nb_v
        self.visual = Image.new("RGBA",
                                (chunk_size * Render.TILE_SIZE * chunk_nb_h,
                                 chunk_size * Render.TILE_SIZE * chunk_nb_v),
                                (0, 0, 0, 0))
        with alive_bar(chunk_nb_h * chunk_nb_v, title="rendering chunks", theme="classic") as render_bar:
            for chunk in map_obj:
                self.render_chunk(chunk)
                render_bar()

    def get_tile_img(self, tile):
        try:
            return self.readers[tile.type].get_tile(tile)
        except KeyError:
            return self.readers["TNF"].get_tile(Render.TNF)

    def draw_tile(self, tile, x, y):
        img = self.get_tile_img(tile)
        dest_box = (x, y, x + Render.TILE_SIZE, y + Render.TILE_SIZE)
        self.visual.paste(img, dest_box, img)

    def render_chunk(self, chunk: Chunk) -> None:
        for layer in chunk.get_layers():
            for (tile_x, tile_y), tile in layer.get_items():
                x, y = chunk.height_map_pos(tile_x, tile_y)
                x *= Render.TILE_SIZE
                y *= Render.TILE_SIZE
                self.draw_tile(tile, x, y)

    # def render_npc(self, layer):
    #     sheet_writer = SpriteSheetWriter(Image.open(os.path.join("resources", "npc.png")), 20, 23)
    #     for tile_x, tile_y in layer.get_ex_pos():
    #         current_tile = layer.get_tile_img((tile_x, tile_y))
    #         try:
    #             sheet_writer.draw_tile(current_tile, self.visual, tile_x * Render.TILE_SIZE, tile_y * Render.TILE_SIZE - 7)
    #         except KeyError:
    #             pass

    def show(self) -> None:
        self.visual.show()

    def save(self, name: str) -> None:
        img_name = name + ".png"
        with alive_bar(1, title="Saving image", theme="classic") as save_bar:
            self.visual.save(os.path.join("saved images", img_name), "png")
            save_bar()
        print("Image saved successfully")
        print(os.path.join(Fore.LIGHTBLUE_EX + os.path.abspath("saved images"), Fore.LIGHTYELLOW_EX + img_name + Style.RESET_ALL))

    def save_prompt(self, seed: Union[int, str] = "") -> None:
        save = input('\n' + Fore.LIGHTBLUE_EX + "Save this image? (y/n/w): " + Style.RESET_ALL)
        file_n = "{} {}".format(datetime.now().strftime("%G-%m-%d %H-%M-%S"), str(seed))
        if save == "y" or save == "w":
            if not os.path.isdir("saved images"):
                os.mkdir("saved images")
            self.save(file_n)
            if save == "w":
                cwd = os.getcwd()
                file_path = os.path.join(cwd, "saved images", file_n + ".png")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)
