from mapClasses import Map, Coordinate
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
    generate_routes(pmap)
    draw_town_map(pmap, tiles_per_pixel)


def generate_routes(pmap: Map, looping_chance: float = 0):
    def is_connected(branches, start, end):
        nodes: set[Coordinate] = {start}
        seen: set[Coordinate] = set()
        while nodes:
            node = nodes.pop()
            if node == end:
                return True

            for branch in branches:
                add_node = None
                if branch[0] == node:
                    add_node = branch[1]
                elif branch[1] == node:
                    add_node = branch[0]

                if add_node and add_node not in seen:
                    nodes.add(add_node)
                    seen.add(node)

        return False

    towns = pmap.towns
    tree: set[tuple[Coordinate, Coordinate]] = set()
    edges = sorted([
        (town1, town2, town1.distance(town2))
        for town1 in towns
        for town2 in towns
        if town1 != town2
    ], key=lambda i: i[2])
    for edge in edges:
        if not is_connected(tree, edge[0], edge[1]):
            tree.add((edge[0], edge[1]))

    for town1, town2 in tree:
        queue: list[tuple[Coordinate, int]] = [(town1, town1.distance(town2))]
        visited: set[Coordinate] = set()
        curr_pos = None
        previous: dict[str, Coordinate] = {str(town1): None}
        while queue and curr_pos != town2:
            curr_pos, curr_dist = queue.pop()
            for pos in curr_pos.udlr():
                if pos not in visited and pos.in_bounds((0, 0), (pmap.chunk_nb_h - 1, pmap.chunk_nb_v - 1)):
                    dist = pos.distance(town2)
                    if dist < curr_dist:
                        queue.append((pos, dist))
                        previous[str(pos)] = curr_pos
                    else:
                        visited.add(pos)
                    visited.add(curr_pos)

            sorted(queue, key=lambda i: i[1])

        route = [town2]
        prev = town2
        while prev is not None:
            prev = previous[str(prev)]
            route.append(prev)

        for chunk_coordinate in route:
            try:
                pmap.chunks[chunk_coordinate.y][chunk_coordinate.x].route = True  # TODO use better type than boolean to indicate n-e-s-w flow of the route in this chunk
            except Exception as e:
                print(e)


def draw_town_map(pmap: Map, tiles_per_pixel: int):
    town_map: Image = Image.new("RGBA", (ceil(pmap.size_h / tiles_per_pixel), ceil(pmap.size_v / tiles_per_pixel)),
                                TMC.water_0)

    image_y = 0
    for y in range(0, pmap.size_v, tiles_per_pixel):
        image_x = 0
        for x in range(0, pmap.size_h, tiles_per_pixel):
            height_sum = 0
            c, _, _ = pmap.parse_to_coordinate_in_chunk(x, y)
            chunk_on_route = c.route is not None
            for j in range(min(tiles_per_pixel, pmap.size_v - y)):
                for i in range(min(tiles_per_pixel, pmap.size_h - x)):
                    height_sum += round(pmap.get_height_map_pos(x + i, y + j) + 0.05)
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

    town_map.show()
