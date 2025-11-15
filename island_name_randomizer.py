from random import randint


def generate_random_name(min_parts: int, max_parts: int) -> str:
    parts_all = ['ba', 'be', 'bi', 'bo', 'bu', 'ca', 'ce', 'ci', 'co', 'cu', 'da', 'de', 'di', 'do', 'du', 'fa', 'fe',
                 'fi', 'fo', 'fu', 'ga', 'ge', 'gi', 'go', 'gu', 'ha', 'he', 'hi', 'ho', 'hu', 'ja', 'je', 'ji', 'jo',
                 'ju', 'ka', 'ke', 'ki', 'ko', 'ku', 'la', 'le', 'li', 'lo', 'lu', 'ma', 'me', 'mi', 'mo', 'mu', 'na',
                 'ne', 'ni', 'no', 'nu', 'pa', 'pe', 'pi', 'po', 'pu', 'qa', 'qe', 'qi', 'qo', 'qu', 'ra', 're', 'ri',
                 'ro', 'ru', 'sa', 'se', 'si', 'so', 'su', 'ta', 'te', 'ti', 'to', 'tu', 'va', 've', 'vi', 'vo', 'vu',
                 'wa', 'we', 'wi', 'wo', 'wu', 'xa', 'xe', 'xi', 'xo', 'xu', 'ya', 'ye', 'yi', 'yo', 'yu', 'za', 'ze',
                 'zi', 'zo', 'zu']
    island_name = ""
    for i in range(randint(min_parts, max_parts)):
        part = parts_all[randint(0, len(parts_all) - 1)]
        island_name += part

    return island_name


name = generate_random_name(2, 4)
if randint(1, 4) == 4:
    name += "-" + generate_random_name(2, 3)

print(f"{name} islands")
