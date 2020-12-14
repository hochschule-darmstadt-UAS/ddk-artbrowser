from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Genre():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):
        allGenreIDs = self.root.findall(paths["Genre_ID_Path"], namespace)
        id = get_id_by_prio(allGenreIDs)

        return id


    def parse(self):
        self.entity_type = 'Genre'
        self.name = []
        self.concepts = []
        self.classifications = []
        for tmp in self.root.findall(paths["Genre_Name_Path"], namespace):
            self.name.append(tmp.text)

        for source_id in self.root.findall(paths["Genre_ID_Path"], namespace):
            concept = SourceID(source_id.text)
            concept._parse_source()
            concept._parse_term(self.root, "Genre_Name_Path", "Genre_Altname_Path")
            self.concepts.append(concept)

        for tmp in self.root.findall(paths["Genre_ClassificationType"], namespace):
            self.classifications.append(tmp.attrib['{http://www.lido-schema.org}type'])


#id string
#type string
#name string[]
#altNames string[] 2
#conceptID SourceID[]
#classificationType string