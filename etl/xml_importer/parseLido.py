import xml.etree.ElementTree as xml
import json
from xpaths import paths

from etl.xml_importer.entities.artwork import Artwork
from etl.xml_importer.lidoObject import LidoObject
from etl.xml_importer.utils.measurement import Measurment
from etl.xml_importer.utils.recordLegal import RecordLegal
from etl.xml_importer.utils.resource import Resource

namespace = {'lido': 'http://www.lido-schema.org'}

artists = dict()
genres = dict()
locations = dict()
materials = dict()
iconographys = dict()

artworks = []

def _parse_lido_file(lidoFile):
    root = xml.parse(lidoFile).getroot()
    #print(root.tag)
    namespace = {'lido': 'http://www.lido-schema.org'}
    lidos = root.findall('lido:lido', namespace)

    for lido in lidos:
        #print(lido)
        parse(lido)

    _print(artworks)

         #lido = LidoObject(lido_xml)
        # print(lido)
         #artworks.append(lido)

def _print(artworks):
    i = 0
    for artwork in artworks:
        print(i, ". Artwork")
        print(artwork.id)
        print(artwork.name)
        print(artwork.types)
        print(artwork.genres)
        print(artwork.location)
        print(artwork.artists)
        print(artwork.iconographies)
        #print(artwork.materials)
        #print(artwork.measurements)
        #print(artwork.recordLegal)
        #print(artwork.resources)
        print()
        i += 1

def parse(lido):
    artwork = Artwork()
    artwork.id = _parse_id(lido)
    artwork.name = _parse_name(lido)
    artwork.types = _parse_types(lido)
    artwork.genres = _parse_genres(lido)
    artwork.location = _parse_location(lido)
    artwork.artists = _parse_artists(lido)
    artwork.iconographies = _parse_iconographies(lido)
    #artwork.materials = _parse_materials(lido)
    #artwork.measurements = _parse_measurements(lido)
    #artwork.recordLegal = _parse_recordLegal(lido)
    #artwork.resources = _parse_resource(lido)

    artworks.append(artwork)

    # artwork.entityType string #TODO: hier fehlt path
    # artwork.inception #TODO: hier fehlt Typ und path

    #TODO: diese Attribute haben eine niedrige Prio, daher erstmal nicht weiter beachten
    # artwork.altName string[] 2
    # artwork.inscriptions string[] 2

def _parse_id(lido):
    id = lido.find(paths["Artwork_Id_Path"], namespace)
    return id.text.replace("/", "-").replace(",", "-")

def _parse_name(lido):
    name = lido.find(paths["Artwork_Name_Path"], namespace)
    return name.text

def _parse_types(lido):
    types = []
    #TODO: ist path richtig? in Excel-Tabelle gibt es keine path
    allTypes = lido.findall(paths["Artwork_Type_Path"], namespace)
    for currentType in allTypes:
        type = currentType.text.split('/')[-1]
        types.append(type)

    return types

def _parse_genres(lido):
    genres = []
    #TODO: sind IDs, so richtig?
    allGenres = lido.findall(paths["Artwork_Genres_Path"], namespace)
    for currentGenre in allGenres:
        genre = currentGenre.text.split('/')[-1]
        genres.append(genre)

    return genres

def _parse_location(lido):
    locations = []
    #TODO: alle Locations fuer das uebergebene lido heraussuchen
    allLocations = lido.findall(paths["Artwork_Location_Path"], namespace)
    for currentLocation in allLocations:
        location = currentLocation.text
        locations.append(location)

    return locations

def _parse_artists(lido):
    artists = []
    allArtists = lido.findall(paths["Artwork_Artists_Path"], namespace)
    for currentArtist in allArtists:
        artist = "ARTIST" #currentArtist #TODO: noch nicht fertig, s. Code von Ahmad
        artists.append(artist)

    return artists

    #Artwork_Artists = self.root.findall(paths["Artwork_Artists_Path"], namespace)
    #Artists = []
    #for actor in Artwork_Artists:
        #für jede Actor find alle Actor_Ids
       # ids = actor.findall('lido:actorInRole/lido:actor/lido:actorID', namespace)
        #for id in ids:
           # if 'getty' in id.text:
                #print(id.text)
            #    Artists.append(id.text.split('/')[-1])
            #    break
            #elif 'gnd' in id.text:
             #   Artists.append(id.text.split('/')[-1])
             #   break
            #elif 'term' in id.text:
             #   Artists.append(id.text.split('/')[-1])
              #  break
           # else:
             #   pass
    #self.artwork["artists"] = Artists

def _parse_iconographies(lido):
    iconographies = []
    allIconographies = lido.findall(paths["Artwork_Iconographies_Path"], namespace)
    for currentIconography in allIconographies:
        iconography = currentIconography.text.split('/')[-1]
        iconographies.append(iconography)

    return iconographies

def _parse_inscription(lido):
    inscriptions = []
    #TODO: alle inscriptions fuer das uebergebene lido heraussuchen
    allInscriptions = lido.findall(paths[""], namespace)
    for currentInscription in allInscriptions:
        inscription = currentInscription.text
        inscriptions.append(inscription)

    return inscriptions

    #inscription_List = self.root.findall(paths["Artwork_Inscription_Path"], namespace)
   # if len(inscription_List) > 0:
       # self.artwork["inscription"] = inscription_List[0].text
   #else:
       # pass

def _parse_materials(lido):
    materials = []
    #TODO: alle Materials fuer das uebergebene lido heraussuchen
    allMaterials = lido.findall(paths[""], namespace)
    for currentMaterial in allMaterials:
        material = "MATERIAL" #currentMaterial
        materials.append(material)

    return materials


####################################################################################

def _parse_measurements(lido):
    measurements = []
    #TODO: alle measurements fuer das uebergebene lido heraussuchen
    measurement = lido.measurement #Typ Measurement
    measurements.append(measurement)

    return measurements

    #measurments_sets = self.root.findall(paths["Artwork_Measurements_Path"], namespace)
    #print(len(measurments_sets))
    #if (len(measurments_sets) > 0):
      #  self.artwork["measurements"].append(Measurment(measurments_sets).getmeasurment())
    #else:
       # pass

def _parse_recordLegal(lido):
    #TODO: recordLegal fuer das uebergebene lido heraussuchen
    recordLegal = lido.recordLegal #Typ RecordLegal

    return recordLegal

    #recordLegal_List = self.root.findall(paths["Artwork_RecordLegal_Path"], namespace)
   #for recordLegal in recordLegal_List:
        #self.artwork["recordLegal"] = RecordLegal(recordLegal).get_recordLegal()

def _parse_resource(lido):
    resources = []
    #TODO: alle resources fuer das uebergebene lido heraussuchen
    resource = lido.resource
    resources.append(resource)

    return resources
    #resourceLegal_List = self.root.findall(paths["Artwork_ResourceLegal_Path"], namespace)
    #if (len(resourceLegal_List) > 0):
       # self.artwork["resourceLegal"] = Resource(resourceLegal_List).getresourceLegal()

def _parse_altName(lido):
    #TODO: altName fuer das uebergebene lido heraussuchen
    altName = lido.altName

    return altName

    #altenames_List = self.root.findall(paths["Artwork_Altename_Path"], namespace)
    #altenames = []
    #if len(altenames_List) > 0:
    #    for altename in  altenames_List:
    #        altenames.append(altename.text)
    #else:
    #    pass
    #self.artwork["altName"] = altenames