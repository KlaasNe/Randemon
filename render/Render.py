import os

from PIL import Image

from .SpriteSheetWriter import *


class Render:
    TILE_SIZE = 16

    def __init__(self, map_obj):
        self.map = map_obj
        self.size = map_obj.chunk_size
        self.visual = Image.new("RGBA", (self.size * Render.TILE_SIZE, self.size * Render.TILE_SIZE), (0, 0, 0, 0))
        for chunk_row in map_obj.chunks:
            for chunk in chunk_row:
                self.render(chunk)

    def render(self, chunk):
        sheet_writer = SpriteSheetWriter()
        tile_buffer = dict()
        for layer in chunk.layers.values():
            for tile_x, tile_y in layer.get_ex_pos():
                current_tile = layer.get_tile(tile_x, tile_y)
                x, y = tile_x * Render.TILE_SIZE, tile_y * Render.TILE_SIZE
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

    def close(self):
        self.visual.close()

    def save(self, name):
        self.visual.save(os.path.join("saved images", name + ".png"), "png")
