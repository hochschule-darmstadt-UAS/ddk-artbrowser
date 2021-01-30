import os
import sys
import ntpath
from operator import attrgetter
import lxml.etree
from etl.xml_importer.entities.artwork import Artwork
import json
from etl.xml_importer.encoding import ComplexJSONEncoder
from etl.xml_importer.entities.artwork import artists, locations, genres, types, materials, iconographies
import logging

artworks = []
artwork_max_count = 0

logging.basicConfig(filename='log_xml_import.log', encoding='utf-8', level=logging.DEBUG)

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
        logging.error("entities must be of type 'list' or 'dict'")
        raise ValueError("entities must be of type 'list' or 'dict'")

    with open(json_filename, "w") as f:
        json.dump(entities_list, f, cls=ComplexJSONEncoder, indent=4)


def rank_artworks(tmp_files, output_dir):
    logging.info('Rank all artworks from temp json files.')
    # read artwork temp json files one by one and add rank (rank = count / artwork_max_count)
    for file in tmp_files:
        output_filename = ntpath.basename(file).replace(".temp", "")

        with open(file) as tmp_json:
            tmp_artworks = json.load(tmp_json)
            for artwork in tmp_artworks:
                artwork['rank'] = artwork['count'] / artwork_max_count

        # write new artworks to final artwork_x.json and delete temporary one
        logging.info("write new artworks to final artwork_x.json and delete temporary one")
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
        for event, elem in lxml.etree.iterparse(lido_file, tag='{http://www.lido-schema.org}lido', events=('end',)):
            logging.info('Read first element from lido file')
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
        logging.info('Write artwork to json.')
        write_to_json(artworks, tmp_file)
        logging.info('Clear artwork.')
        artworks.clear()

    logging.info('Rank artists.')
    rank_entities(artists)
    logging.info('Write artist to json')
    write_to_json(artists, "{}/artists.json".format(output_dir))
    logging.info('Clear artist.')
    artists.clear()

    logging.info('Rank genres.')
    rank_entities(genres)
    logging.info('Write genres to json.')
    write_to_json(genres, "{}/genres.json".format(output_dir))
    logging.info('Clear genres.')
    genres.clear()

    logging.info('Rank iconographies.')
    rank_entities(iconographies)
    logging.info('Write iconographies to json.')
    write_to_json(iconographies, "{}/iconographies.json".format(output_dir))
    logging.info('Clear iconographies.')
    iconographies.clear()

    logging.info('Rank locations.')
    rank_entities(locations)
    logging.info('Write locations to json.')
    write_to_json(locations, "{}/locations.json".format(output_dir))
    logging.info('Clear locations.')
    locations.clear()

    logging.info('Rank materials.')
    rank_entities(materials)
    logging.info('Write materials to json.')
    write_to_json(materials, "{}/materials.json".format(output_dir))
    logging.info('Clear materials.')
    materials.clear()

    logging.info('Rank types.')
    rank_entities(types)
    logging.info('Write types to json.')
    write_to_json(types, "{}/types.json".format(output_dir))
    logging.info('Clear types.')
    types.clear()

    rank_artworks(tmp_files, output_dir)  # count is done in artwork class itself


