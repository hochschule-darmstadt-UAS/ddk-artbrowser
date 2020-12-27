from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Genre():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):
        genre_id = self.root.findall(paths["Genre_ID_Path"], namespace)
        if len(genre_id) > 0:
            id = get_id_by_prio(genre_id)
        else:
            id = self.root.find(paths["Genre_Label_Path"], namespace).text
        return id


    def parse(self):
        self.entity_type = 'Genre'
        self.label = self.root.find(paths["Genre_Label_Path"], namespace).text
        #self.concepts = []
        self.classificationType = self.root.attrib['{http://www.lido-schema.org}type']

'''
        for source_id in self.root.findall(paths["Genre_ID_Path"], namespace):
            concept = SourceID(source_id)
            concept._parse_source()
            concept._parse_term(self.root, "Genre_Label_Path", "Genre_Altname_Path")
            self.concepts.append(concept)
'''



#id string
#type string
#name string[]
#altNames string[] 2
#conceptID SourceID[]
#classificationType string