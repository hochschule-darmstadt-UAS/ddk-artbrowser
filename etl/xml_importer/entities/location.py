from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import namespace, paths

class Location():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()
        self.type = 'location'
        self.name = self._parse_id()
        # self.altNames = self._parse_altNames() # #TODO: methode definieren(prio3)
        # self.inventoryNumber = self._parse_inventoryNumber() # #TODO: methode definieren(prio2)
        self.placeID = self.sourceID() ##enthält source,id,term
        self.placeName = self.placeName()
        # self.placeAltNames = self.placeAltNames() # #TODO: methode definieren(prio3)

    def _parse_id(self):
        id = self.root.findall(paths["Location_ID_Path"], namespace)[0]
        return id.text

    def sourceID(self):
        sourceIdRoot = self.root.findall(paths["Location_SourceID_Path"], namespace)[0]# repositoryLocation
        # print(sourceid)
        return SourceID(sourceIdRoot)

    def placeName(self):
        placeName = self.root.findall(paths["Location_PlaceName_Path"], namespace)
        return placeName[0]

    def parse(self):
        pass
#id
#entityType string
#name string
#altNames string[] 3
#inventoryNumber string 2
#placeID SourceID[]
#placeName  string[]
#placeAltNames string[] 3