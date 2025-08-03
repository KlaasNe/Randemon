from timeit import timeit
from mapStructure.pkmnMap import PkmnMap


class PkmnMapFactory:

    @staticmethod
    @timeit
    def create_pkmn_map(chunk_nb_h: int,
                        chunk_nb_v: int,
                        chunk_size: int,
                        seed: int,
                        max_buildings: int = 16,
                        island: bool = False,
                        make_height_map: bool = False,
                        themed_towns: bool = True,
                        terrain_chaos: int = 4,
                        max_height: int = 6,
                        town_map: str = None
                        ) -> PkmnMap:
        pkmn_map: PkmnMap = PkmnMap(
            chunk_nb_h,
            chunk_nb_v,
            chunk_size,
            seed,
            max_buildings,
            island,
            make_height_map,
            themed_towns,
            terrain_chaos,
            max_height,
            town_map
        )
        pkmn_map.create()

        return pkmn_map
