import ctypes
import os
from datetime import datetime
from typing import Union

from PIL import Image
from colorama import Fore, Style

from pkmnMap.Chunk import Chunk
from pkmnMap import PkmnMap
from pkmnMap.tiles.Tile import Tile
from render.SpriteSheetReaders import *
from timeit import timeit
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import io


class Render:
    TILE_SIZE = 16
    TNF = Tile("TNF", 0, 0)

    def __init__(self):
        self.readers: dict = dict()
        self.visual: Image = None
        for reader in SpriteSheetReaders:
            self.readers[reader.name] = reader.value

    @timeit
    def export_to_tmx_with_csv(self, pkmn_map: PkmnMap):
        for chunk in pkmn_map:
            self.export_chunk_to_tmx_with_csv(chunk)

    def export_chunk_to_tmx_with_csv(self, chunk: Chunk):
        with open(os.path.join("render", "randemon_chunk_template.tmx"), "r") as template:
            chunk_xml_tree: ET.ElementTree = ET.parse(template)
            chunk_xml_root = chunk_xml_tree.getroot()
            layer_id: int = 1
            for layer in chunk.get_layers():
                matrix = np.zeros((chunk.size, chunk.size), dtype=int)
                for x, y in layer.get_ex_pos():
                    tile: Tile = layer[(x, y)]
                    tiled_id = self.readers[tile.type].get_tiled_id(tile)
                    matrix[y][x] = tiled_id

                csv_buffer = io.StringIO()
                pd.DataFrame(matrix).to_csv(csv_buffer, header=False, index=False)

                lines = csv_buffer.getvalue().split("\n")
                for i in range(len(lines) - 2):
                    lines[i] = lines[i].strip("\r") + ","

                csv_string_with_trailing_commas = "\n".join(lines)

                layer_xml = ET.SubElement(chunk_xml_root, "layer", attrib={"id": str(layer_id), "name": layer.name, "width": str(chunk.size), "height": str(chunk.size)})
                data = ET.SubElement(layer_xml, "data", attrib={"encoding": "csv"})
                data.text = csv_string_with_trailing_commas

                layer_id += 1

        with open(os.path.join("render", "tiled_output", f"randemon_chunk_x{chunk.chunk_x}_y{chunk.chunk_y}.tmx"), "wb+") as f:
            chunk_xml_tree.write(f.name, xml_declaration=True, encoding="UTF-8")

    @timeit
    def render(self, pkmn_map: PkmnMap, town_map_pos: str):
        town_map_scale = 8
        chunk_size = pkmn_map.chunk_size
        chunk_nb_h, chunk_nb_v = pkmn_map.chunk_nb_h, pkmn_map.chunk_nb_v
        size = (chunk_size * Render.TILE_SIZE * chunk_nb_h, chunk_size * Render.TILE_SIZE * chunk_nb_v)
        self.visual = Image.new("RGBA", size, (0, 0, 0, 0))
        for chunk in pkmn_map:
            self.render_chunk(chunk)

        if pkmn_map.town_map_img is not None:
            self.paste_town_map(pkmn_map, town_map_pos, scale=town_map_scale)

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

    def paste_town_map(self, pkmn_map: PkmnMap, pos: str, scale: int = 8):
        town_map: Image = pkmn_map.town_map_img
        w, h = town_map.size
        nw, nh = w * scale, h * scale
        town_map = town_map.resize((nw, nh), 0)

        self_img_w, self_img_h = self.visual.size
        if pos == 'TOPLEFT':
            self.visual.paste(town_map, (0, 0, nw, nh))
        elif pos == 'TOPRIGHT':
            self.visual.paste(town_map, (self_img_w - nw, 0, self_img_w, nh))
        elif pos == 'BOTTOMLEFT':
            self.visual.paste(town_map, (0, self_img_h - nh, nw, self_img_h))
        elif pos == 'BOTTOMRIGHT':
            self.visual.paste(town_map, (self_img_w - nw, self_img_h - nh, self_img_w, self_img_h))

    # def render_npc(self, Layer):
    #     sheet_writer = SpriteSheetWriter(Image.open(os.path.join("resources", "npc.png")), 20, 23)
    #     for tile_x, tile_y in Layer.get_ex_pos():
    #         current_tile = Layer.get_tile_img((tile_x, tile_y))
    #         try:
    #             sheet_writer.draw_tile(current_tile, self.visual, tile_x * Render.TILE_SIZE, tile_y * Render.TILE_SIZE - 7)
    #         except KeyError:
    #             pass

    def show(self) -> None:
        if self.visual is not None:
            self.visual.show()

    def save(self, name: str, directory: str) -> None:
        img_name = name + ".png"
        self.visual.save(os.path.join(directory, img_name), "png")
        print("Image saved successfully")
        print(os.path.join(Fore.LIGHTBLUE_EX + os.path.abspath(directory),
                           Fore.LIGHTYELLOW_EX + img_name + Style.RESET_ALL))

    def save_prompt(self, seed: Union[int, str] = "", directory: str = "saved_images") -> None:
        save = input('\n' + Fore.LIGHTBLUE_EX + "Save this image? (y/[n]/w): " + Style.RESET_ALL)
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
