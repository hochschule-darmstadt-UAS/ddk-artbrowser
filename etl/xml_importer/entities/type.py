from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import namespace, paths


class Type():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):
        allTypeIDs = self.root.findall(paths["Type_ID_Path"], namespace)
        id = get_id_by_prio(allTypeIDs)

        return id

    def parse(self):
        self.entity_type = "Type"
        self.name = []
        self.concepts = []
        for tmp in self.root.findall(paths["Type_Name_Path"], namespace):
            self.name.append(tmp.text)

        for source_id in self.root.findall(paths["Type_ID_Path"], namespace):
            concept = SourceID(source_id)
            concept._parse_source()
            concept._parse_term(self.root, "Type_Name_Path", "Type_Altname_Path")
            self.concepts.append(concept)


#altNames string[] 2
