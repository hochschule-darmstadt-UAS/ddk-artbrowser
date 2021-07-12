from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.parseLido import sanitize, filter_none
from etl.xml_importer.encoding import JSONEncodable


class Iconography(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'iconography'
        self._parse_id()

        self.label = ""
        self.alt_labels = []
        self.iconclass = ""
        self.source_ids = []

        self.count = 1
        self.rank = 0

    def _parse_id(self):
        id_root = self.root.find(paths["Iconography_Id_Path"], namespace)
        if id_root is not None:
            id = id_root.text.split('/')[-1]
            self.id = id
        else:
            self.id = ""

        # we do not add a prefix to the iconography ID
        # because the ID is the iconclass and therefore should not be altered

    def parse(self):
        self._parse_source_ids()
        self._parse_label()
        self._parse_alt_labels()
        self._parse_iconclass()

    def _parse_label(self):
        label_root = self.root.find(paths["Iconography_Label_Path"], namespace)
        if label_root is not None and label_root.text is not None:
            self.label = sanitize(label_root.text)
        else:
            self.label = ""

    def _parse_alt_labels(self):
        for alt_label_root in self.root.findall(paths['Iconography_Alt_Label_Path'], namespace):
            if alt_label_root.text is None:
                continue
            alt_label = sanitize(alt_label_root.text)
            self.alt_labels.append(alt_label)

    def _parse_iconclass(self):
        iconclass_root = self.root.find(paths["Iconography_Iconclass_Path"], namespace)
        if iconclass_root is not None:
            self.iconclass = iconclass_root.text
        else:
            self.iconclass = ""

    def _parse_source_ids(self):
        self.source_ids = []
        for source_id in self.root.findall(paths["Iconography_Id_Path"], namespace):
            concept = SourceID(source_id)
            self.source_ids.append(concept)

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "altLabels": self.alt_labels,
            "sourceIDs": self.source_ids,
            "count": self.count,
            "rank": self.rank,
        }
        return filter_none(json)
