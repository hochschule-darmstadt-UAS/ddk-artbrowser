from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Material():

    def __init__(self, root):
        self.root = root
        self.entity_type = 'Material'
        self.label = ""
        self.source_ids = []

        self.id = self._parse_id()

    def parse(self):
        self.label = self._parse_label()
        self.source_ids = self._parse_sourceIDs()

    def _parse_id(self):
        all_material_ids = self.root.findall(paths["Material_ID_Path"], namespace)
        id = get_id_by_prio(all_material_ids)

        return id

    def _parse_label(self):
        return self.root.findall(paths["Material_name_Path"], namespace)[0].text

    def _parse_sourceIDs(self):
        source_ids = []
        for source_id in self.root.findall(paths["Material_ID_Path"], namespace):
            concept = SourceID(source_id)
            source_ids.append(concept)

        return source_ids

    def __json_repr__(self):
        return {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "sourceID": self.source_ids,
        }


#id
#entityType string
#conceptID SourceID[]
#name string
#altNames string[] 2