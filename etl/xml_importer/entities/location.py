from etl.xml_importer.parseLido import sanitize_location, sanitize, filter_none
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import namespace, paths
from etl.xml_importer.encoding import JSONEncodable


class Location(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'location'
        self._parse_id()

        self.label = ""
        self.alt_labels = []
        self.inventoryNumber = ""
        self.source_ids = []
        self.placeLabel = ""
        self.placeAltLabels = []

        self.count = 1
        self.rank = 0

    def _parse_id(self):
        # The location id is either the label or the place label
        self._parse_label()
        if self.label is None:
            self._parse_placeLabel()
            location_id = self.placeLabel
        else:
            location_id = self.label

        self.id = sanitize_location(location_id)

        if self.id:
            # add entity type as id prefix to ensure uniqueness
            self.id = self.entity_type + "-" + self.id

    def parse(self):
        self._parse_label()
        self._parse_alt_labels()
        self._parse_inventoryNumber()
        self._parse_placeLabel()
        self._parse_placeAltLabel()
        self._parse_source_ids()

    def _parse_label(self):
        label_root = self.root.find(paths["Location_Label_Path"], namespace)
        if label_root is not None:
            self.label = sanitize(label_root.text)
        else:
            self._parse_placeLabel()
            self.label = self.placeLabel

    def _parse_alt_labels(self):
        self.alt_labels = []
        alt_label_roots = self.root.findall(paths["Location_Label_Path"], namespace)
        if len(alt_label_roots) > 1:
            for alt_label_root in alt_label_roots[1:]:
                self.alt_labels.append(sanitize(alt_label_root.text))

    def _parse_inventoryNumber(self):
        inventoryNumber_root = self.root.find(paths["Location_InventoryNumber_Path"], namespace)
        if inventoryNumber_root is not None:
            self.inventoryNumber = inventoryNumber_root.text
        else:
            self.inventoryNumber =None

    def _parse_placeLabel(self):
        place_label_root = self.root.find(paths["Location_PlaceLabel_Path"], namespace)
        if place_label_root is not None:
            self.placeLabel = sanitize(place_label_root.text)
        else:
            self.placeLabel = ""

    def _parse_placeAltLabel(self):
        self.placeAltLabels = []
        placeAltLabel_roots = self.root.findall(paths["Location_PlaceLabel_Path"], namespace)
        if len(placeAltLabel_roots) > 1:
            for placeAltLabel_root in placeAltLabel_roots[1:]:
                self.placeAltLabels.append(sanitize(placeAltLabel_root.text))

    def _parse_source_ids(self):
        for source_id_root in self.root.findall(paths["Location_PlaceID_Path"], namespace):
            source_id = SourceID(source_id_root)
            self.source_ids.append(source_id)

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "altLabels": self.alt_labels,
            "inventoryNumber": self.inventoryNumber,
            "sourceIDs": self.source_ids,
            "placeLabel": self.placeLabel,
            "placeAltLabels": self.placeAltLabels,
            "count": self.count,
            "rank": self.rank,
        }
        return filter_none(json)
