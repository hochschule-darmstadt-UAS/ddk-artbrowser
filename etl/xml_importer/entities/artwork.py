from etl.xml_importer.xpaths import paths

from etl.xml_importer.entities.artist import Artist
from etl.xml_importer.entities.genre import Genre
from etl.xml_importer.entities.iconography import Iconography
from etl.xml_importer.entities.material import Material
from etl.xml_importer.entities.type import Type
from etl.xml_importer.entities.location import Location
from etl.xml_importer.utils.recordLegal import RecordLegal
from etl.xml_importer.utils.resource import Resource
from etl.xml_importer.utils.measurement import Measurement
from etl.xml_importer.xpaths import namespace

from etl.xml_importer.parseLido import sanitize_id, sanitize

from etl.xml_importer.encoding import JSONEncodable

artists = dict()
genres = dict()
locations = dict()
materials = dict()
iconographies = dict()
types = dict()


class Artwork(JSONEncodable):

    def __init__(self, lido):
        self.lido = lido
        self.entity_type = "artwork"

        self.id = self._parse_id()
        self.label = self._parse_label()
        self.inception = self._parse_inception()
        self.inscriptions = self._parse_inscription()
        self.types = self._parse_types()
        self.genres = self._parse_genres()
        self.location = self._parse_location()
        self.artists = self._parse_artists()
        self.iconographies = self._parse_iconographies()
        self.materials = self._parse_materials()
        self.measurements = self._parse_measurements()
        self.recordLegal = self._parse_recordLegal()
        self.resources = self._parse_resource()

    # TODO: diese Attribute haben eine niedrige Prio, daher erstmal nicht weiter beachten
    # artwork.altName string[] 2
    # artwork.inscriptions string[] 2

    def _parse_id(self):
        # TODO: Was soll ich hier nur lido herausnehmen?: DE - Mb112 - lido - t3 - 000230
        #         88 - T - 001 - T - 065
        id = self.lido.find(paths["Artwork_Id_Path"], namespace).text
        id = sanitize_id(id)
        id = id.replace("/", "-").replace(",", "-").replace("lido-", "").replace("obj-", "")
        return id

    def _parse_label(self):  # TODO: Format DE-Mb112-00000000001
        label = self.lido.find(paths["Artwork_Name_Path"], namespace)
        if label is not None:
            return sanitize(label.text)
        else:
            return ""

    def _parse_inception(self):
        event_display_date = self.lido.find(paths['Artwork_Inception_Path'], namespace)
        if event_display_date is not None:
            return event_display_date.text
        else:
            return ""

    def _parse_inscription(self):
        inscriptions = []
        all_inscriptions = self.lido.findall(paths["Artwork_Inscription_Path"], namespace)
        for inscription in all_inscriptions:
            inscriptions.append(inscription.text)

        return inscriptions

    def _parse_types(self):
        type_ids = []
        for typeRoot in self.lido.findall(paths["Artwork_Type_Path"], namespace):
            type_ = Type(typeRoot)
            type_ids.append(type_.id)

            if type_.id not in types:
                type_.parse()
                types[type_.id] = type_

        return type_ids

    def _parse_genres(self):
        genre_ids = []
        for genreRoot in self.lido.findall(paths["Artwork_Genre_Path"], namespace):
            genre = Genre(genreRoot)
            genre_ids.append(genre.id)

            if genre.id not in genres:
                genre.parse()
                genres[genre.id] = genre

        return genre_ids

    def _parse_location(self):
        location_ids = []
        for locationRoot in self.lido.findall(paths["Artwork_Location_Path"], namespace):
            location = Location(locationRoot)
            location_ids.append(location.id)

            if location.id not in locations:
                location.parse()
                locations[location.id] = location

        return location_ids

    def _parse_artists(self):
        artist_ids = []
        for artistRoot in self.lido.findall(paths["Artwork_Artists_Path"], namespace):
            artist = Artist(artistRoot)
            artist_ids.append(artist.id)

            if artist.id not in artists:
                artist.parse()
                artists[artist.id] = artist
        return artist_ids

    def _parse_iconographies(self):
        iconography_ids = []
        for iconographyRoot in self.lido.findall(paths["Artwork_Iconographies_Path"], namespace):
            iconography = Iconography(iconographyRoot)
            iconography_ids.append(iconography.id)

            if iconography.id not in iconographies:
                iconography.parse()
                iconographies[iconography.id] = iconography

        return iconography_ids

    def _parse_materials(self):
        material_ids = []
        for material_root in self.lido.findall(paths["Artwork_Materials_Path"], namespace):
            material = Material(material_root)
            material_ids.append(material.id)

            if material.id not in materials:
                material.parse()
                materials[material.id] = material

        return material_ids

    ####################################################################################

    def _parse_measurements(self):
        measurements = []

        measurements_sets = self.lido.findall(paths["Artwork_Measurements_Path"], namespace)
        for measurement_root in measurements_sets:
            measurement = Measurement(measurement_root)
            # for now only append if the measurement has a display text (to prevent empty measurements)
            if measurement.displayName != "":
                measurements.append(measurement)

        return measurements

    def _parse_recordLegal(self):
        recordLegal_root = self.lido.find(paths["Artwork_RecordLegal_Path"], namespace)
        if recordLegal_root is not None:
            return RecordLegal(recordLegal_root)
        else:
            return None

    def _parse_resource(self):
        allresources = []

        for resource in self.lido.findall(paths["Artwork_Resource_Path"], namespace):
            allresources.append(Resource(resource))

        return allresources
        # resourceLegal_List = self.root.findall(paths["Artwork_ResourceLegal_Path"], namespace)
        # if (len(resourceLegal_List) > 0):
        # self.artwork["resourceLegal"] = Resource(resourceLegal_List).getresourceLegal()

    def _parse_altName(lido):
        # TODO
        raise NotImplementedError

        # altenames_List = self.root.findall(paths["Artwork_Altename_Path"], namespace)
        # altenames = []
        # if len(altenames_List) > 0:
        #    for altename in  altenames_List:
        #        altenames.append(altename.text)
        # else:
        #    pass
        # self.artwork["altName"] = altenames

    def __json_repr__(self):
        return {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "measurements": self.measurements,
            "recordLegal": self.recordLegal,
            "resources": self.resources,
            "types": self.types,
            "genres": self.genres,
            "locations": self.location,
            "iconographies": self.iconographies,
            "inscriptions": self.inscriptions,
            "inceptions": self.inception,
        }
