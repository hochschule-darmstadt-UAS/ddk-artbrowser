from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Material():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()
        self.type = 'type'
        self.conceptID = self._parse_conceptID()
        self.name = self._parse_name()

    def _parse_id(self):
        allMaterilIDs = self.root.findall(paths["Material_ID_Path"], namespace)
        id = get_id_by_prio(allMaterilIDs)

    def _parse_conceptID(self):
        allMaterials = []
        for material in self.root.findall(paths["Material_ID_Path"], namespace):
            allMaterials.append(SourceID(material))
        return allMaterials

    def _parse_name(self):
        return self.root.findall(paths["Material_name_Path"], namespace)[0].text

    def parse(self):
        pass

#id
#entityType string
#conceptID SourceID[]
#name string
#altNames string[] 2