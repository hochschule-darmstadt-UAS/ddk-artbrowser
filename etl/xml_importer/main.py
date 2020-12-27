from lxml import etree as xml
from etl.xml_importer.entities.artwork import Artwork
import json
from etl.xml_importer.encoding import ComplexJSONEncoder

artworks = []

if __name__ == '__main__':
    lidoFile = 'merged.xml'
    root = xml.parse(lidoFile).getroot()
    # print(root.tag)
    namespace = {'lido': 'http://www.lido-schema.org'}
    lidos = root.findall('lido:lido', namespace)

    for lido in lidos:
        artwork = Artwork(lido)
        artworks.append(artwork)

    for artwork in artworks:
        print(json.dumps(artwork, cls=ComplexJSONEncoder, indent=4))

    #_print_artworks(artworks[0:1])



