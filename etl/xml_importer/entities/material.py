from etl.xml_importer.parseLido import get_id_by_prio, filter_none, sanitize_id
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.encoding import JSONEncodable


class Material(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'material'
        self.label = ""
        self.source_ids = []

        self._parse_id()

        self.count = 1
        self.rank = 0

    def parse(self):
        self._parse_label()
        self._parse_sourceIDs()

    def _parse_id(self):
        all_material_ids = self.root.findall(paths["Material_ID_Path"], namespace)
        if len(all_material_ids) > 0:
            self.id = get_id_by_prio(all_material_ids)
        else:
            self._parse_label()
            self.id = self.label

        # add entity type as id prefix to ensure uniqueness
        self.id = sanitize_id(self.id)
        self.id = self.entity_type + "-" + self.id

    def _parse_label(self):
        self.label = self.root.findall(paths["Material_name_Path"], namespace)[0].text

    def _parse_sourceIDs(self):
        for source_id in self.root.findall(paths["Material_ID_Path"], namespace):
            concept = SourceID(source_id)
            self.source_ids.append(concept)

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "sourceIDs": self.source_ids,
            "count": self.count,
            "rank": self.rank,
        }
        return filter_none(json)
