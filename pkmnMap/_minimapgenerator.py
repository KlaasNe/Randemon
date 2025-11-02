import os

from pkmnMap import Coordinate
from PIL import Image
from math import ceil


TILE_SIZE = 8
TILE_SHEET_DIRECTORY = os.path.join("render", "tileSheets")


class TMC:  # Town Map Colors
    land_1 = "#188008"
    land_2 = "#38a808"
    land_3 = "#50c808"
    land_4 = "#70e020"
    land_5 = "#a8f038"
    land_1_route = "#e0a000"
    land_2_route = "#e8b838"
    land_3_route = "#f0d050"
    land_4_route = "#e8e070"
    land_5_route = "#f0e888"
    water_0 = "#98d0f8"
    water_1 = "#a0b0f8"
    water_0_route = "#58a8e0"
    water_1_route = "#5090d0"
    water_0_route_special = "#e0d8a0"
    water_1_route_special = "#c8c890"

    @staticmethod
    def rgb_from_hex(hex: str):
        h = hex.lstrip('#')
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def generate_mini_map(self) -> None:
    tiles_per_pixel = self.chunk_size // 8
    self.town_map_img = _draw_mini_map(self, tiles_per_pixel)


def _draw_mini_map(pkmn_map, tiles_per_pixel: int):
    town_map: Image = Image.new("RGBA", (ceil(pkmn_map.size_h / tiles_per_pixel), ceil(pkmn_map.size_v / tiles_per_pixel)), TMC.water_0)
    image_y = 0
    for y in range(0, pkmn_map.size_v, tiles_per_pixel):
        image_x = 0
        for x in range(0, pkmn_map.size_h, tiles_per_pixel):
            height_sum = 0
            c, _, _ = pkmn_map.parse_to_coordinate_in_chunk(x, y)
            chunk_on_route = any(c.route)
            for j in range(min(tiles_per_pixel, pkmn_map.size_v - y)):
                for i in range(min(tiles_per_pixel, pkmn_map.size_h - x)):
                    height_sum += round(pkmn_map.get_height_map_pos(x + i, y + j))
            avg_height = height_sum // (tiles_per_pixel ** 2)
            color = None
            if avg_height > 0:
                if avg_height == 1:
                    color = TMC.land_1 if not chunk_on_route else TMC.land_1_route
                elif avg_height == 2:
                    color = TMC.land_2 if not chunk_on_route else TMC.land_2_route
                elif avg_height == 3:
                    color = TMC.land_3 if not chunk_on_route else TMC.land_3_route
                elif avg_height == 4:
                    color = TMC.land_4 if not chunk_on_route else TMC.land_4_route
                elif avg_height >= 5:
                    color = TMC.land_5 if not chunk_on_route else TMC.land_5_route
            else:
                if image_y % 2 == 0:
                    color = TMC.water_1 if not chunk_on_route else TMC.water_1_route
                elif chunk_on_route:
                    color = TMC.water_0_route

            if color:
                town_map.putpixel((image_x, image_y), TMC.rgb_from_hex(color))
            image_x += 1
        image_y += 1

    with Image.open(os.path.join(TILE_SHEET_DIRECTORY, "townMap.png")).convert("RGBA") as marker:
        marker.load()
        for town in pkmn_map.towns:
            dest_box = (town.x * 8, town.y * 8, town.x * 8 + TILE_SIZE, town.y * 8 + TILE_SIZE)
            town_map.paste(marker, dest_box, marker)

    # town_map.save(os.path.join("saved_images", "{} {}__townMap.png".format(datetime.now().strftime("%G-%m-%d %H-%M-%S"), str(pmap.seed))), "png")
    return town_map
