from etl.xml_importer.parseLido import sanitize_location, sanitize, filter_none
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import namespace, paths
from etl.xml_importer.encoding import JSONEncodable


class Location(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'location'
        self.id = self._parse_id()

        self.label = ""
        self.source_ids = []
        self.placeLabel = ""

    def _parse_id(self):
        # The location id is either the label or the place label
        location_id = self._parse_label()
        if location_id == "":
            location_id = self._parse_placeLabel()

        return sanitize_location(location_id)

    def parse(self):
        self.label = self._parse_label()
        self.placeLabel = self._parse_placeLabel()
        self.source_ids = self._parse_source_ids()

    def _parse_label(self):
        label_root = self.root.find(paths["Location_Label_Path"], namespace)
        if label_root is not None:
            return sanitize_location(label_root.text)
        else:
            return ""

    def _parse_placeLabel(self):
        place_label_root = self.root.find(paths["Location_PlaceLabel_Path"], namespace)
        if place_label_root is not None:
            return sanitize(place_label_root.text)
        else:
            return ""

    def _parse_source_ids(self):
        source_ids = []
        for source_id_root in self.root.findall(paths["Location_PlaceID_Path"], namespace):
            source_id = SourceID(source_id_root)
            source_ids.append(source_id)

        return source_ids

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "sourceIDs": self.source_ids,
            "placeLabel": self.placeLabel,
        }
        return filter_none(json)
