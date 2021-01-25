from etl.xml_importer.parseLido import get_id_by_prio, filter_none, sanitize_id, sanitize
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.encoding import JSONEncodable


class Genre(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'genre'
        self._parse_id()

        self.label = ""
        self.alt_labels = []
        self.source_ids = []
        self.classificationType = ""

        self.count = 1
        self.rank = 0

    def _parse_id(self):
        genre_id = self.root.findall(paths["Genre_ID_Path"], namespace)
        if len(genre_id) > 0:
            id = get_id_by_prio(genre_id)
        else:
            id = self.root.find(paths["Genre_Label_Path"], namespace).text

        id = sanitize_id(id)
        # add entity type as id prefix to ensure uniqueness
        self.id = self.entity_type + "-" + id

    def parse(self):
        self.label = sanitize(self.root.find(paths["Genre_Label_Path"], namespace).text)
        self._parse_alt_labels()
        self.classificationType = self.root.attrib['{http://www.lido-schema.org}type']
        self._parse_source_ids()

    def _parse_alt_labels(self):
        self.alt_labels = []
        for alt_label_root in self.root.findall(paths["Genre_AltLabel_Path"], namespace):
            self.alt_labels.append(sanitize(alt_label_root.text))

    def _parse_source_ids(self):
        self.source_ids = []
        for source_id_root in self.root.findall(paths["Genre_ID_Path"], namespace):
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
            "sourceIDs": self.source_ids,
            "classificationType": self.classificationType,
            "count": self.count,
            "rank": self.rank,
        }
        return filter_none(json)
