from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.xpaths import namespace, paths


class SourceID():

    def __init__(self, root):
        self.root = root
#source string
#id string
#term string