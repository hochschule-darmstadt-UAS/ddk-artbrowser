import xml.etree.ElementTree as xml
import json
import copy
import xpaths
import entities



artists = dict()
genres = dict()
locations = dict()
materials = dict()
iconographys = dict()

artworks = []
def parse_lido(lido):
    artwork = entities.Artwork(lido)
    artworks[artwork.id] = artwork


if __name__ == '__main__':
    data = 'merged.xml'
    root = xml.parse(data).getroot()
    namespace = {'lido': 'http://www.lido-schema.org'}
    lidos = root.findall('lido:lido', namespace)
    for lido_xml in lidos:
        lido = entities.LidoObject(lido_xml).artwork
        artworks.append(lido)


    print(artworks)


    




