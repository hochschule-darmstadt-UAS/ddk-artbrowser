from lxml import etree as xml
from etl.xml_importer.entities.artwork import Artwork
import json
from etl.xml_importer.encoding import ComplexJSONEncoder
from etl.xml_importer.entities.artwork import artists, locations, genres, types, materials, iconographys

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
    lidoFile = 'merged_lido_1.xml'
    root = xml.parse(lidoFile).getroot()
    # print(root.tag)
    namespace = {'lido': 'http://www.lido-schema.org'}
    lidos = root.findall('lido:lido', namespace)

    for lido in lidos:
        artwork = Artwork(lido)
        artworks.append(artwork)

    write_to_json(artworks, "/tmp/artworks.json")
    write_to_json(artists, "/tmp/artists.json")
    write_to_json(genres, "/tmp/genres.json")
    write_to_json(iconographys, "/tmp/iconographys.json")
    write_to_json(locations, "/tmp/locations.json")
    write_to_json(materials, "/tmp/materials.json")
    write_to_json(types, "/tmp/types.json")
