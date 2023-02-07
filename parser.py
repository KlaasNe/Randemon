import random
from argparse import ArgumentParser
from sys import maxsize


def make_parser() -> ArgumentParser:
    """Make the ArgParser object."""
    parser = ArgumentParser(
        description='Landscape generator using the tileset of pokemon fire red')

    parser.add_argument(
        '--chunk-size',
        dest='chunk_size',
        type=int,
        default=50,
        help='The number of tiles a chunk consists of.')

    parser.add_argument(
        '--ch',
        dest='chunks_horizontal',
        type=int,
        default=4,
        help='The number of chunks horizontally.')

    parser.add_argument(
        '--cv',
        dest='chunks_vertical',
        type=int,
        default=4,
        help='The number of chunks vertically.')

    parser.add_argument(
        '--s',
        dest='save_opt',
        action='store_true',
        help='Save generated image.')

    parser.add_argument(
        '--seed',
        dest='seed',
        type=int,
        default=random.randint(0, maxsize),
        help='The world generation seed')

    parser.add_argument(
        '--max-height',
        dest='max_height',
        type=int,
        default=6,
        help='Maximal height of a hill')

    parser.add_argument(
        '--height-map',
        dest='height_map_opt',
        action='store_true',
        help='Generate a heightmap instead of a regular map.'
    )

    parser.add_argument(
        '--max-buildings',
        dest='max_buildings',
        type=int,
        default=16,
        help='Define the maximum amount of buildings for a chunk 0 for none, Pokécenter\nGym and Pokémart are'
             ' not included in this argument.'
    )

    parser.add_argument(
        '--themed-towns',
        dest='themed_towns_opt',
        action='store_true',
        help='Have towns generated in predefined themes instead of picking random houses.'
    )

    parser.add_argument(
        '--mainland',
        dest='mainland_opt',
        action='store_true',
        help='Generate an plain land with rivers instead of an island.'
    )

    parser.add_argument(
        '--no-show',
        dest='no_show_opt',
        action='store_true',
        help="Don't show the generated image."
    )

    parser.add_argument(
        '--terrain-chaos',
        dest='terrain_chaos',
        type=int,
        default=4,
        help='Determine the chaos in the terrain generation process. A higher value means more chaos. Default is 4.'
    )

    parser.add_argument(
        '--save-directory',
        dest='save_directory',
        type=str,
        default="saved_images",
        help='Choose a directory where the generated image should be saved. Has to be an existing directory.'
    )

    return parser
