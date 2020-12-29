from lxml import etree as xml
from etl.xml_importer.entities.artwork import Artwork
import json
from etl.xml_importer.encoding import ComplexJSONEncoder
from etl.xml_importer.entities.artwork import artists, locations, genres, types, materials, iconographies

artworks = []


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


if __name__ == '__main__':
    lidoFile = '../data_samples/object.xml'
    root = xml.parse(lidoFile).getroot()
    # print(root.tag)
    namespace = {'lido': 'http://www.lido-schema.org'}
    lidos = root.findall('lido:lido', namespace)

    for lido in lidos:
        artwork = Artwork(lido)
        artworks.append(artwork)

    write_to_json(artworks, "./output/artworks.json")
    write_to_json(artists, "./output/artists.json")
    write_to_json(genres, "./output/genres.json")
    write_to_json(iconographies, "./output/iconographies.json")
    write_to_json(locations, "./output/locations.json")
    write_to_json(materials, "./output/materials.json")
    write_to_json(types, "./output/types.json")
