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

from etl.xml_importer.parseLido import sanitize_id, sanitize, filter_none

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
        self.count = 0

        self._parse_id()
        self._parse_label()
        self._parse_inception()
        self._parse_inscription()
        self._parse_types()
        self._parse_genres()
        self._parse_location()
        self._parse_artists()
        self._parse_iconographies()
        self._parse_materials()
        self._parse_measurements()
        self._parse_recordLegal()
        self._parse_resource()

        self.calc_count()

        self.clear()

    # TODO: diese Attribute haben eine niedrige Prio, daher erstmal nicht weiter beachten
    # artwork.altName string[] 2
    # artwork.inscriptions string[] 2

    def _parse_id(self):
        # TODO: Was soll ich hier nur lido herausnehmen?: DE - Mb112 - lido - t3 - 000230
        #         88 - T - 001 - T - 065
        id = self.lido.find(paths["Artwork_Id_Path"], namespace).text
        id = sanitize_id(id)
        id = id.replace("/", "-").replace(",", "-").replace("lido-", "").replace("obj-", "")

        self.id = self.entity_type + "-" + id

    def _parse_label(self):  # TODO: Format DE-Mb112-00000000001
        label = self.lido.find(paths["Artwork_Name_Path"], namespace)
        if label is not None:
            self.label = sanitize(label.text)
        else:
            self.label = None

    def _parse_inception(self):
        event_display_date = self.lido.find(paths['Artwork_Inception_Path'], namespace)
        if event_display_date is not None:
            self.inception = event_display_date.text
        else:
            self.inception = None

    def _parse_inscription(self):
        self.inscriptions = []
        all_inscriptions = self.lido.findall(paths["Artwork_Inscription_Path"], namespace)
        for inscription in all_inscriptions:
            self.inscriptions.append(inscription.text)

    def _parse_types(self):
        self.types = []
        for typeRoot in self.lido.findall(paths["Artwork_Type_Path"], namespace):
            type_ = Type(typeRoot)
            if not type_.id:
                continue

            self.types.append(type_.id)

            if type_.id not in types:
                type_.parse()
                type_.clear()
                types[type_.id] = type_
                del type_
            else:
                # increase count
                types[type_.id].count += 1

    def _parse_genres(self):
        self.genres = []
        for genreRoot in self.lido.findall(paths["Artwork_Genre_Path"], namespace):
            genre = Genre(genreRoot)
            if not genre.id:
                continue

            self.genres.append(genre.id)

            if genre.id not in genres:
                genre.parse()
                genre.clear()
                genres[genre.id] = genre
                del genre
            else:
                # increase count
                genres[genre.id].count += 1

    def _parse_location(self):
        self.locations = []
        for locationRoot in self.lido.findall(paths["Artwork_Location_Path"], namespace):
            location = Location(locationRoot)
            if not location.id:
                continue

            self.locations.append(location.id)

            if location.id not in locations:
                location.parse()
                location.clear()
                locations[location.id] = location
                del location
            else:
                # increase count
                locations[location.id].count += 1

    def _parse_artists(self):
        self.artists = []
        for artistRoot in self.lido.findall(paths["Artwork_Artists_Path"], namespace):
            artist = Artist(artistRoot)
            if not artist.id:
                continue

            self.artists.append(artist.id)

            if artist.id not in artists:
                artist.parse()
                artist.clear()
                artists[artist.id] = artist
                del artist
            else:
                # increase count
                artists[artist.id].count += 1

    def _parse_iconographies(self):
        self.iconographies = []
        for iconographyRoot in self.lido.findall(paths["Artwork_Iconographies_Path"], namespace):
            iconography = Iconography(iconographyRoot)
            # ignore iconographies without id (e.g. merged_lido_1.xml, line 6118)
            if iconography.id == "":
                continue

            self.iconographies.append(iconography.id)

            if iconography.id not in iconographies:
                iconography.parse()
                iconography.clear()
                iconographies[iconography.id] = iconography
                del iconography
            else:
                # increase count
                iconographies[iconography.id].count += 1

    def _parse_materials(self):
        self.materials = []
        for material_root in self.lido.findall(paths["Artwork_Materials_Path"], namespace):
            material = Material(material_root)
            if not material.id:
                continue
            self.materials.append(material.id)

            if material.id not in materials:
                material.parse()
                material.clear()
                materials[material.id] = material
                del material
            else:
                # increase count
                materials[material.id].count += 1

    ####################################################################################

    def _parse_measurements(self):
        self.measurements = []

        measurements_sets = self.lido.findall(paths["Artwork_Measurements_Path"], namespace)
        for measurement_root in measurements_sets:
            measurement = Measurement(measurement_root)
            # for now only append if the measurement has a display text (to prevent empty measurements)
            if measurement.displayName != "":
                self.measurements.append(measurement)

    def _parse_recordLegal(self):
        recordLegal_root = self.lido.find(paths["Artwork_RecordLegal_Path"], namespace)
        if recordLegal_root is not None:
            self.recordLegal = RecordLegal(recordLegal_root)
        else:
            self.recordLegal = None

    def _parse_resource(self):
        self.resources = []

        for resource in self.lido.findall(paths["Artwork_Resource_Path"], namespace):
            self.resources.append(Resource(resource))

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

    def calc_count(self):
        self.count = len(self.artists) + len(self.iconographies) + len(self.types) + len(self.genres) + len(self.materials) + \
            len(self.locations) + len(self.resources) + len(self.inscriptions)
        if self.recordLegal:
            self.count += 1
        if self.label:
            self.count += 1
        if self.inception:
            self.count += 1

    def clear(self):
        del self.lido

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "measurements": self.measurements,
            "recordLegal": self.recordLegal,
            "resources": self.resources,
            "artists": self.artists,
            "materials": self.materials,
            "types": self.types,
            "genres": self.genres,
            "locations": self.locations,
            "iconographies": self.iconographies,
            "inscriptions": self.inscriptions,
            "inceptions": self.inception,
            "count": self.count
        }
        return filter_none(json)
