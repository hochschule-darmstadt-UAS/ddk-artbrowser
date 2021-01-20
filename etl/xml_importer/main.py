import os
import sys
import ntpath
from operator import attrgetter
import lxml.etree
from etl.xml_importer.entities.artwork import Artwork
import json
from etl.xml_importer.encoding import ComplexJSONEncoder
from etl.xml_importer.entities.artwork import artists, locations, genres, types, materials, iconographies

artworks = []
artwork_max_count = 0


def get_input_xml_files(input_dir):
    xml_files = ["{}/{}".format(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.xml')]
    return sorted(xml_files)


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


def rank_artworks(tmp_files, output_dir):
    # read artwork temp json files one by one and add rank (rank = count / artwork_max_count)
    for file in tmp_files:
        output_filename = ntpath.basename(file).replace(".temp", "")

        with open(file) as tmp_json:
            tmp_artworks = json.load(tmp_json)
            for artwork in tmp_artworks:
                artwork['rank'] = artwork['count'] / artwork_max_count

        # write new artworks to final artwork_x.json and delete temporary one
        write_to_json(tmp_artworks, "{}/{}".format(output_dir, output_filename))
        os.remove(file)


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

    if len(sys.argv) < 3:
        print("Usage: {} <input-directory> <output-directory>".format(sys.argv[0]))
        exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    num_of_files = 2
    file_count = 0
    lido_files = get_input_xml_files(input_dir)
    tmp_files = []
    for lido_file in lido_files:
        file_count += 1
        # get the xml filename without .xml extension
        base_filename = ntpath.basename(os.path.splitext(lido_file)[0])

        print("Processing file {} / {}: {}".format(file_count, len(lido_files), lido_file))
        # TODO: Change base path of lidoFile
        for event, elem in lxml.etree.iterparse(lido_file, tag='{http://www.lido-schema.org}lido', events=('end',)):
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
        tmp_file = "{}/artworks_{}.temp.json".format(output_dir, base_filename)
        tmp_files.append(tmp_file)
        write_to_json(artworks, tmp_file)
        artworks.clear()

    rank_entities(artists)
    write_to_json(artists, "{}/artists.json".format(output_dir))
    artists.clear()

    rank_entities(genres)
    write_to_json(genres, "{}/genres.json".format(output_dir))
    genres.clear()

    rank_entities(iconographies)
    write_to_json(iconographies, "{}/iconographies.json".format(output_dir))
    iconographies.clear()

    rank_entities(locations)
    write_to_json(locations, "{}/locations.json".format(output_dir))
    locations.clear()

    rank_entities(materials)
    write_to_json(materials, "{}/materials.json".format(output_dir))
    materials.clear()

    rank_entities(types)
    write_to_json(types, "{}/types.json".format(output_dir))
    types.clear()

    rank_artworks(tmp_files, output_dir)  # count is done in artwork class itself


