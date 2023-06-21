import ctypes
import os
from datetime import datetime
from typing import Union

from PIL import Image
from alive_progress import alive_bar
from colorama import Fore, Style

from mapClasses import Tile, Map
from mapClasses.chunk import Chunk
from render.SpriteSheetReaders import *


class Render:
    TILE_SIZE = 16
    TNF = Tile("TNF", 0, 0)

    def __init__(self):
        self.readers: dict = dict()
        self.visual: Image = None
        for reader in SpriteSheetReaders:
            self.readers[reader.name] = reader.value

    def render(self, map_obj: Map):
        chunk_size = map_obj.chunk_size
        chunk_nb_h, chunk_nb_v = map_obj.chunk_nb_h, map_obj.chunk_nb_v
        size = (chunk_size * Render.TILE_SIZE * chunk_nb_h, chunk_size * Render.TILE_SIZE * chunk_nb_v)
        self.visual = Image.new("RGBA", size, (0, 0, 0, 0))
        with alive_bar(chunk_nb_h * chunk_nb_v, title="rendering chunks", theme="classic") as render_bar:
            for chunk in map_obj:
                self.render_chunk(chunk)
                render_bar()

    def get_tile_img(self, tile: Tile) -> Image:
        try:
            return self.readers[tile.type].get_tile(tile)
        except KeyError:
            return self.readers["TNF"].get_tile(Render.TNF)

    def draw_tile(self, tile: Tile, x: int, y: int) -> None:
        img = self.get_tile_img(tile)
        dest_box = (x, y, x + Render.TILE_SIZE, y + Render.TILE_SIZE)
        self.visual.paste(img, dest_box, img)

    def render_chunk(self, chunk: Chunk) -> None:
        for layer in chunk.get_layers():
            for (tile_x, tile_y), tile in layer:
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

    def save(self, name: str, directory: str) -> None:
        img_name = name + ".png"
        with alive_bar(1, title="Saving image", theme="classic") as save_bar:
            self.visual.save(os.path.join(directory, img_name), "png")
            save_bar()
        print("Image saved successfully")
        print(os.path.join(Fore.LIGHTBLUE_EX + os.path.abspath(directory),
                           Fore.LIGHTYELLOW_EX + img_name + Style.RESET_ALL))

    def save_prompt(self, seed: Union[int, str] = "", directory: str = "saved_images") -> None:
        save = input('\n' + Fore.LIGHTBLUE_EX + "Save this image? (y/n/w): " + Style.RESET_ALL)
        file_n = "{}_{}".format(datetime.now().strftime("%G-%m-%d_%H-%M-%S"), str(seed))
        if save == "y" or save == "w":
            if not os.path.isdir(directory):
                if directory == "saved_images":
                    os.mkdir(directory)
                else:
                    print(Fore.RED + "The given directory doesn't exist" + Style.RESET_ALL)
                    exit(-1)
            self.save(file_n, directory)
            if save == "w":
                cwd = os.getcwd()
                file_path = os.path.join(cwd, "saved_images", file_n + ".png")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)
