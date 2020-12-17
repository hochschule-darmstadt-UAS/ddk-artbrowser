from etl.xml_importer.lidoObject import namespace
from etl.xml_importer.utils.rights import Rights
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths


class RecordLegal:
    def __init__(self, root):
        self.root = root
        self.record_ids = self._parse_id()
        self.record_types = self._parse_type()
        self.record_source = self._parse_source()
        #self.rights	= Rights() #Einfaches Objekt von Rights
        self.record_info_link = self._parse_info_link()

    def _parse_id(self): #TODO:
        record_ids = []
        for id_root in self.root.findall(paths["RecordLegal_RecordID_Path"], namespace):
            record_id = SourceID(id_root)
            record_id.source = "SOURCE" #._parse_source()
            record_ids.append(record_id)

        return record_ids

    def _parse_type(self):
        record_types = []
        for type_root in self.root.findall(paths["RecordType_ID_Path"], namespace):
            record_type = SourceID(type_root)
            record_type._parse_term(self.root, "RecordType_Term_Path", None)

        return record_types

    def _parse_source(self):
        source = self.root.find(paths["RecordLegal_Source_Path"], namespace).text
        return source

    def _parse_info_link(self):
        record_info_links = []
        for info_link in self.root.findall(paths["RecordLegal_RecordInfoLink_Path"], namespace):
            record_info_links.append(info_link.text)

        return record_info_links