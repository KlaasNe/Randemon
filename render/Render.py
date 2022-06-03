import ctypes
import os
from colorama import Fore
from colorama import Style
from datetime import datetime

from PIL import Image

from .SpriteSheetWriter import *
from alive_progress import alive_bar


class Render:
    TILE_SIZE = 16

    def __init__(self, map_obj):
        self.map = map_obj
        self.size = map_obj.chunk_size
        self.visual = Image.new("RGBA",
                                (self.size * Render.TILE_SIZE * self.map.chunk_nb_h,
                                 self.size * Render.TILE_SIZE * self.map.chunk_nb_v),
                                (0, 0, 0, 0))
        self.tile_buffer = dict()
        with alive_bar(self.map.chunk_nb_h * self.map.chunk_nb_v, title="rendering chunks", theme="classic") as render_bar:
            cy = 0
            for chunk_row in self.map.chunks:
                cx = 0
                for chunk in chunk_row:
                    self.render(chunk, cx, cy)
                    render_bar()
                    cx += 1
                cy += 1

    def render(self, chunk, cx, cy):
        sheet_writer = SpriteSheetWriter()
        for layer in chunk.layers.values():
            for tile_x, tile_y in layer.get_ex_pos():
                current_tile = layer.get_tile(tile_x, tile_y)
                x, y = tile_x * TILE_SIZE, tile_y * TILE_SIZE
                c_offset_x, c_offset_y = cx * TILE_SIZE * chunk.size, cy * TILE_SIZE * chunk.size
                x += c_offset_x
                y += c_offset_y
                try:
                    img = self.tile_buffer[current_tile]
                    sheet_writer.draw_img(img, self.visual, x, y)
                except KeyError:
                    self.tile_buffer[current_tile] = sheet_writer.draw_tile(current_tile, self.visual, x, y)

    # def render_npc(self, layer):
    #     sheet_writer = SpriteSheetWriter(Image.open(os.path.join("resources", "npc.png")), 20, 23)
    #     for tile_x, tile_y in layer.get_ex_pos():
    #         current_tile = layer.get_tile_img((tile_x, tile_y))
    #         try:
    #             sheet_writer.draw_tile(current_tile, self.visual, tile_x * Render.TILE_SIZE, tile_y * Render.TILE_SIZE - 7)
    #         except KeyError:
    #             pass

    def show(self):
        self.visual.show()

    def save(self, name):
        img_name = name + ".png"
        self.visual.save(os.path.join("saved images", img_name), "png")
        print("Image saved successfully")
        print(os.path.join(Fore.LIGHTBLUE_EX + os.path.abspath("saved images"), Fore.LIGHTYELLOW_EX + img_name + Style.RESET_ALL))

    def save_prompt(self, map_obj):
        save = input('\n' + Fore.LIGHTBLUE_EX + "Save this image? (y/n/w): " + Style.RESET_ALL)
        if save == "y" or save == "w":
            file_n = "{} {}".format(datetime.now().strftime("%G-%m-%d %H-%M-%S"), map_obj.seed)
            if not os.path.isdir("saved images"):
                os.mkdir("saved images")
            self.save(file_n)
            if save == "w":
                cwd = os.getcwd()
                file_path = os.path.join(cwd, "saved images", file_n + ".png")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)
