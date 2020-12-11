from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Iconography():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()
        self.type = 'iconography'
        self.conceptID = self._parse_conceptID()
        self.name = self._parse_name()
        #print(self.name)

    def _parse_id(self):
        allIconographiesIDs = self.root.find(paths["Icongraphy_Id_Path"], namespace)
        return allIconographiesIDs.text.split('/')[-1]

    def _parse_conceptID(self):
        allConceptIDs = []
        for conceptID in self.root.findall(paths["Icongraphy_Id_Path"], namespace):
            allConceptIDs.append(SourceID(conceptID))
        return allConceptIDs

    def _parse_name(self):
        return self.root.find(paths["Icongraphy_Name_Path"], namespace).text

    def parse(self):
        pass
#id
#entityType string
#conceptID SourceID[]
#name string
#altNames string[] 2