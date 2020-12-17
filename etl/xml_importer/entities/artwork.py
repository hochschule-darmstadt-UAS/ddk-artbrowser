from xpaths import paths

from etl.xml_importer.entities.artist import Artist
from etl.xml_importer.entities.genre import Genre
from etl.xml_importer.entities.iconography import Iconography
from etl.xml_importer.entities.material import Material
from etl.xml_importer.entities.type import Type
from etl.xml_importer.entities.location import Location
from etl.xml_importer.utils.recordLegal import RecordLegal
from etl.xml_importer.utils.resource import Resource
from etl.xml_importer.xpaths import namespace

artists = dict()
genres = dict()
locations = dict()
materials = dict()
iconographys = dict()
types = dict()

class Artwork():

    def __init__(self, lido):
        self.lido = lido
        self.id = self._parse_id()
        self.name = self._parse_name()
        self.inscriptions = self._parse_inscription()
        self.types = self._parse_types()
        self.genres = self._parse_genres()
        self.location = self._parse_location()
        self.artists = self._parse_artists()
        self.iconographies = self._parse_iconographies()
        self.materials = self._parse_materials()
        #self.measurements = _parse_measurements()
        self.recordLegal = self._parse_record_legal()
        self.resources = self._parse_resource()

    #TODO: diese Attribute haben eine niedrige Prio, daher erstmal nicht weiter beachten
    # artwork.altName string[] 2
    # artwork.inscriptions string[] 2


    def _parse_id(self):
        # TODO: Was soll ich hier nur lido herausnehmen?: DE - Mb112 - lido - t3 - 000230
        #         88 - T - 001 - T - 065
        id = self.lido.find(paths["Artwork_Id_Path"], namespace). text
        id = id.replace("/", "-").replace(",", "-").replace("lido-", "").replace("obj-", "")
        return id

    def _parse_name(self):
        name = self.lido.find(paths["Artwork_Name_Path"], namespace).text
        return name

    def _parse_inscription(self):
        inscriptions = []
        allInscriptions = self.lido.findall(paths["Artwork_Inscription_Path"], namespace)
        for currentInscription in allInscriptions:
            inscription = currentInscription.text
            inscriptions.append(inscription)

        return inscriptions

    def _parse_types(self):
        typeIDs = []
        for typeRoot in self.lido.findall(paths["Artwork_Type_Path"], namespace):
            type_ = Type(typeRoot)
            typeIDs.append(type_.id)

            if type_.id not in types:
                type_.parse()
                types[type_.id] = type_

        return typeIDs

    def _parse_genres(self):
        genreIDs = []
        for genreRoot in self.lido.findall(paths["Artwork_Genre_Path"], namespace):
            genre_ = Genre(genreRoot)
            genreIDs.append(genre_.id)

            if genre_.id not in genres:
                genre_.parse()
            genres[genre_.id] = genre_
        #print(genreIDs)
        #print(genres)
        return genreIDs

    def _parse_location(self):
        locations = []
        for locationRoot in self.lido.findall(paths["Artwork_Location_Path"], namespace):
            location_ = Location(locationRoot)
            locations.append(location_.id)

            if location_.id not in locations:
                location_.parse()
                locations[location_.id] = location_

        #print(locationIDs)
        #print(locations)
        return locations[0]

    def _parse_artists(self):
        artistIDs = []
        for artistRoot in self.lido.findall(paths["Artwork_Artists_Path"], namespace):
            artist_ = Artist(artistRoot)
            artistIDs.append(artist_.id)

            if artist_.id not in artists:
                artist_.parse()
                artists[artist_.id] = artist_
        return artistIDs

    def _parse_iconographies(self):
        iconographyIDs = []
        for iconographyRoot in self.lido.findall(paths["Artwork_Iconographies_Path"], namespace):
            iconography_ = Iconography(iconographyRoot)
            iconographyIDs.append(iconography_.id)

            if iconography_.id not in iconographys:
                iconography_.parse()
                iconographys[iconography_.id] = iconography_
        return iconographyIDs

    def _parse_materials(self):
        materialIDs = []
        for material in self.lido.findall(paths["Artwork_Materials_Path"], namespace):
            material_ = Material(material)
            materialIDs.append(material_.id)

            if material_.id not in materials:
                material_.parse()
                materials[material_.id] = material_
        return materialIDs


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

    def _parse_record_legal(self):
        record_legal_root = self.lido.find(paths["Artwork_RecordLegal_Path"], namespace)
        record_legal = RecordLegal(record_legal_root)

        return record_legal

    def _parse_resource(self):
        allresources = []

        for resource in self.lido.findall(paths["Artwork_Resource_Path"], namespace):
            allresources.append(Resource(resource))

        return allresources
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
