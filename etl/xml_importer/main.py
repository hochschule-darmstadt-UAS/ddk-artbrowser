import os
from operator import attrgetter
import lxml.etree
from etl.xml_importer.entities.artwork import Artwork
import json
from etl.xml_importer.encoding import ComplexJSONEncoder
from etl.xml_importer.entities.artwork import artists, locations, genres, types, materials, iconographies

artworks = []
artwork_max_count = 0


def write_to_json(entities, json_filename):
    entities_list = None
    if isinstance(entities, list):
        entities_list = entities
    elif isinstance(entities, dict):
        entities_list = list(entities.values())
    else:
        raise ValueError("entities must be of type 'list' or 'dict'")

    with open(json_filename, "w") as f:
        json.dump(entities_list, f, cls=ComplexJSONEncoder, indent=4)


def rank_artworks(lim_i):
    # read artwork temp json files one by one and add rank (rank = count / artwork_max_count)
    for i in range(1, lim_i):
        with open('output/artworks_{}.temp.json'.format(i)) as tmp_json:
            tmp_artworks = json.load(tmp_json)
            for artwork in tmp_artworks:
                artwork['rank'] = artwork['count'] / artwork_max_count

        # write new artworks to final artwork_x.json and delete temporary one
        write_to_json(tmp_artworks, "output/artworks_{}.json".format(i))
        os.remove('output/artworks_{}.temp.json'.format(i))


def rank_entities(entities: dict):
    max_count = max(entities.values(), key=attrgetter('count')).count
    for id, entity in entities.items():
        entity.rank = entity.count / max_count


"""
    http://lxml.de/parsing.html#modifying-the-tree
    Based on Liza Daly's fast_iter
    http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    See also http://effbot.org/zone/element-iterparse.htm
"""
if __name__ == '__main__':
    namespace = {'lido': 'http://www.lido-schema.org'}

    num_of_files = 1
    for i in range(1, num_of_files+1):
        print("Processing file ", i)
        # TODO: Change base path of lidoFile
        lidoFile = "merged.xml"
        for event, elem in lxml.etree.iterparse(lidoFile, tag='{http://www.lido-schema.org}lido', events=('end',)):
            artwork = Artwork(elem)

            artworks.append(artwork)
            if artwork.count > artwork_max_count:
                artwork_max_count = artwork.count
            del artwork

            # It's safe to call clear() here because no descendants will be accessed
            elem.clear()
            # Also eliminate now-empty references from the root node to elem
            for ancestor in elem.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]

        # to save memory we write the artworks of a single xml file to one artwork_x.temp.json file
        # these files will be used in the rank_artworks() function afterwards to create the final artwork json files
        write_to_json(artworks, "./output/artworks_{}.temp.json".format(i))
        artworks.clear()

    rank_entities(artists)
    write_to_json(artists, "./output/artists.json")
    artists.clear()

    rank_entities(genres)
    write_to_json(genres, "./output/genres.json")
    genres.clear()

    rank_entities(iconographies)
    write_to_json(iconographies, "./output/iconographies.json")
    iconographies.clear()

    rank_entities(locations)
    write_to_json(locations, "./output/locations.json")
    locations.clear()

    rank_entities(materials)
    write_to_json(materials, "./output/materials.json")
    materials.clear()

    rank_entities(types)
    write_to_json(types, "./output/types.json")
    types.clear()

    rank_artworks(num_of_files + 1)  # count is done in artwork class itself


