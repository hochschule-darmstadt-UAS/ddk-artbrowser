from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import namespace, paths

class Location():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):
        return self.root.findall(paths["Location_ID_Path"], namespace)[0].text

    def parse(self):
        self.entity_type = 'Location'
        self.name = []
        self.concepts = []
        self.placeName = self.root.findall(paths["Location_PlaceName_Path"], namespace)[0].text

        for tmp in self.root.findall(paths["Location_ID_Path"], namespace):
            self.name.append(tmp.text)

        for source_id in self.root.findall(paths["Location_SourceID_Path"], namespace):##ToDo:kann ein Objekt kein lido:placeID haben.Soll es in SourceID kontrolliert werden
            concept = SourceID(source_id.text)
            concept._parse_source()
            concept._parse_term(self.root, "Location_Name_Path", "Location_Altname_Path")##ToDo:beide haben gleichen Path.SourceID soll erklaert werden
            self.concepts.append(concept)



#id
#entityType string
#name string
#altNames string[] 3
#inventoryNumber string 2
#placeID SourceID[]
#placeName  string[]
#placeAltNames string[] 3