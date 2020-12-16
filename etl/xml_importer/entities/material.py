from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Material():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):
        allMaterilIDs = self.root.findall(paths["Material_ID_Path"], namespace)
        id = get_id_by_prio(allMaterilIDs)

        return id

    def parse(self):
        self.entity_type = 'Material'
        self.name = self.root.findall(paths["Material_name_Path"], namespace)[0].text
        self.concepts = []
        for source_id in self.root.findall(paths["Material_ID_Path"], namespace):
            concept = SourceID(source_id)
            concept._parse_source()
            concept._parse_term(self.root, "Material_name_Path", "Material_Altname_Path")
            self.concepts.append(concept)


#id
#entityType string
#conceptID SourceID[]
#name string
#altNames string[] 2