#import entities
import xml.etree.ElementTree as xml
from xpaths import paths
from etl.xml_importer.entities.artwork import Artwork

artworks = []

def _print_artworks(artworks):
    i = 0
    for artwork in artworks:
        print(i, ". Artwork")
        print("ID: ", artwork.id)
        print("Name: ", artwork.name)
        print("Inscriptions: ", artwork.inscriptions)
        print(artwork.types)
        # print(artwork.genres)
        # print(artwork.location)
        # print(artwork.artists)
        # print(artwork.iconographies)
        # print(artwork.materials)
        # print(artwork.measurements)
        # print(artwork.recordLegal)
        # print(artwork.resources)
        print()
        i += 1

if __name__ == '__main__':
    lidoFile = 'merged.xml'
    root = xml.parse(lidoFile).getroot()
    # print(root.tag)
    namespace = {'lido': 'http://www.lido-schema.org'}
    lidos = root.findall('lido:lido', namespace)

    for lido in lidos:
        artwork = Artwork(lido)
        artworks.append(artwork)

    _print_artworks(artworks)



