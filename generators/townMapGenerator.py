from mapClasses import Map
from PIL import Image
from math import ceil


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


def generate_town_map(pmap: Map, tiles_per_pixel: int):
    town_map: Image = Image.new("RGBA", (ceil(pmap.size_h / tiles_per_pixel), ceil(pmap.size_v / tiles_per_pixel)), TMC.water_0)

    image_y = 0
    for y in range(0, pmap.size_v, tiles_per_pixel):
        image_x = 0
        for x in range(0, pmap.size_h, tiles_per_pixel):
            height_sum = 0
            for j in range(min(tiles_per_pixel, pmap.size_v - y)):
                for i in range(min(tiles_per_pixel, pmap.size_h - x)):
                    height_sum += round(pmap.get_height_map_pos(x + i, y + j) + 0.05)
            avg_height = height_sum // (tiles_per_pixel ** 2)
            color = None
            if avg_height > 0:
                if avg_height == 1:
                    color = TMC.land_1
                elif avg_height == 2:
                    color = TMC.land_2
                elif avg_height == 3:
                    color = TMC.land_3
                elif avg_height == 4:
                    color = TMC.land_4
                elif avg_height >= 5:
                    color = TMC.land_5
            else:
                if y % 2 == 0:
                    color = TMC.water_1
            if color:
                town_map.putpixel((image_x, image_y), TMC.rgb_from_hex(color))
            image_x += 1
        image_y += 1

    town_map.show()
