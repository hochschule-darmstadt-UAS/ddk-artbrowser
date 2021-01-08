import os
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


def fast_iter(context, func, *args, **kwargs):
    """
    http://lxml.de/parsing.html#modifying-the-tree
    Based on Liza Daly's fast_iter
    http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    See also http://effbot.org/zone/element-iterparse.htm
    """
    for event, elem in context:
        func(elem, *args, **kwargs)
        # It's safe to call clear() here because no descendants will be
        # accessed
        elem.clear()
        # Also eliminate now-empty references from the root node to elem
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context


def parse_artwork(elem):
    global artwork_max_count
    artwork = Artwork(elem)
    artworks.append(artwork)
    if artwork.count > artwork_max_count:
        artwork_max_count = artwork.count
    del artwork


if __name__ == '__main__':
    namespace = {'lido': 'http://www.lido-schema.org'}

    num_of_files = 41
    for i in range(1, num_of_files+1):
        print("Processing file ", i)
        lidoFile = '/home/yannick/Downloads/openArtBrowser-Projekt/ddb_20190606/merged_lido_{}.xml'.format(i)
        context = lxml.etree.iterparse(lidoFile, tag='{http://www.lido-schema.org}lido', events=('end',))
        fast_iter(context, parse_artwork)

        # to save memory we write the artworks of a single xml file to one artwork_x.temp.json file
        # these file will be used in the rank_artworks() function afterwards to create the final artwork json files
        write_to_json(artworks, "./output/artworks_{}.temp.json".format(i))
        artworks.clear()

    rank_artworks(num_of_files+1)     # count is done in artwork class itself
    # TODO: Implement count_and_rank_x()
    # count_and_rank_artists()
    # count_and_rank_genres()
    # count_and_rank_iconographies()
    # count_and_rank_location()
    # count_and_rank_materials()
    # count_and_rank_types()

    write_to_json(artists, "./output/artists.json")
    write_to_json(genres, "./output/genres.json")
    write_to_json(iconographies, "./output/iconographies.json")
    write_to_json(locations, "./output/locations.json")
    write_to_json(materials, "./output/materials.json")
    write_to_json(types, "./output/types.json")



