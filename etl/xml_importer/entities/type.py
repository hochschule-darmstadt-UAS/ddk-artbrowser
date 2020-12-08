from etl.xml_importer.parseLido import get_id_by_prio
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
        pass


#id string
#entityType string
#name string[]
#altNames string[] 2
#conceptID SourceID[]