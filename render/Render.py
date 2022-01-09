import ctypes
import os
from datetime import datetime

from PIL import Image

from .SpriteSheetWriter import *


class Render:
    TILE_SIZE = 16

    def __init__(self, map_obj):
        self.map = map_obj
        self.size = map_obj.chunk_size
        self.visual = Image.new("RGBA",
                                (self.size * Render.TILE_SIZE * self.map.chunk_nb_h,
                                 self.size * Render.TILE_SIZE * self.map.chunk_nb_v),
                                (0, 0, 0, 0))
        cy = 0
        for chunk_row in self.map.chunks:
            cx = 0
            for chunk in chunk_row:
                self.render(chunk, cx, cy)
                cx += 1
            cy += 1

    def render(self, chunk, cx, cy):
        sheet_writer = SpriteSheetWriter()
        tile_buffer = dict()
        for layer in chunk.layers.values():
            for tile_x, tile_y in layer.get_ex_pos():
                current_tile = layer.get_tile(tile_x, tile_y)
                x, y = tile_x * Render.TILE_SIZE, tile_y * Render.TILE_SIZE
                c_offset_x, c_offset_y = cx * Render.TILE_SIZE * chunk.size, cy * Render.TILE_SIZE * chunk.size
                x += c_offset_x
                y += c_offset_y
                if current_tile in tile_buffer:
                    SpriteSheetWriter.draw_img(tile_buffer[current_tile], self.visual, x, y)
                else:
                    img = sheet_writer.draw_tile(current_tile, self.visual, x, y)
                    tile_buffer[current_tile] = img

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
        self.visual.save(os.path.join("saved images", name + ".png"), "png")

    def save_prompt(self, map_obj):
        save = input("Save this image? (y/n/w): ")
        if save == "y" or save == "w":
            file_n = "{} {}".format(datetime.now().strftime("%G-%m-%d %H-%M-%S"), map_obj.seed)
            if not os.path.isdir("saved images"):
                os.mkdir("saved images")
            self.save(file_n)
            if save == "w":
                cwd = os.getcwd()
                file_path = os.path.join(cwd, "saved images", file_n + ".png")
                ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)
