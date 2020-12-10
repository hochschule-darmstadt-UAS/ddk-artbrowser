from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Genre():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()
        self.type = 'genre'
        self.name = self._parse_name()[0]
        self.altname = self._parse_name()[1:]
        self.classificationType = self._parse_classificationType() ##ToDo:muss erklaeret werden, Liste oder eine rausziehen
        self.sourceID = self._parse_sourceID()

    def _parse_id(self):
        allGenreIDs = self.root.findall(paths["Genre_ID_Path"], namespace)
        id = get_id_by_prio(allGenreIDs)
        return id

    def _parse_name(self):
        allGenreNames = []
        root = self.root.findall(paths["Genre_Name_Path"], namespace)
        for name in root:
            allGenreNames.append(name.text)
        return allGenreNames

    def _parse_classificationType(self):
        classificationType = self.root.findall(paths["Genre_ClassificationType"], namespace)
        return classificationType

    def _parse_sourceID(self):
        sourceId = self.root.find(paths["Genre_ID_Path"], namespace)
        return SourceID(sourceId)

    def parse(self):
        pass
#id string
#type string
#name string[]
#altNames string[] 2
#conceptID SourceID[]
#classificationType string