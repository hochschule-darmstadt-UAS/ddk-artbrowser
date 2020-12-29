from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Genre():

    def __init__(self, root):
        self.root = root
        self.entity_type = 'Genre'
        self.id = self._parse_id()

        self.label = ""
        self.source_ids = []
        self.classificationType = ""

    def _parse_id(self):
        genre_id = self.root.findall(paths["Genre_ID_Path"], namespace)
        if len(genre_id) > 0:
            id = get_id_by_prio(genre_id)
        else:
            id = self.root.find(paths["Genre_Label_Path"], namespace).text
        return id

    def parse(self):
        self.label = self.root.find(paths["Genre_Label_Path"], namespace).text
        self.source_ids = self._parse_source_ids()
        self.classificationType = self.root.attrib['{http://www.lido-schema.org}type']

    def _parse_source_ids(self):
        source_ids = []
        for source_id_root in self.root.findall(paths["Genre_ID_Path"], namespace):
            source_id = SourceID(source_id_root)
            source_ids.append(source_id)

        return source_ids

    def __json_repr__(self):
        return {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "sourceID": self.source_ids,
            "classificationType": self.classificationType,
        }

'''
        
'''



#id string
#type string
#name string[]
#altNames string[] 2
#conceptID SourceID[]
#classificationType string