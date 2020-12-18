from etl.xml_importer.parseLido import sanitize_location
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import namespace, paths

class Location():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):
        location_id = self.root.find(paths["Location_Label_Path"], namespace).text
        return sanitize_location(location_id)

    def parse(self):
        self.entity_type = 'Location'
        self.label= self.root.find(paths["Location_Label_Path"], namespace).text
        self.concepts = []
        self.placeLabel = self.root.find(paths["Location_PlaceLabel_Path"], namespace).text

        for source_id in self.root.findall(paths["Location_PlaceID_Path"], namespace):
            concept = SourceID(source_id)
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