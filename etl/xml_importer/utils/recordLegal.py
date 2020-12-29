from etl.xml_importer.xpaths import namespace
from etl.xml_importer.utils.rights import Rights
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths


class RecordLegal:
    def __init__(self, root):
        self.root = root
        self.record_ids = self._parse_id()
        self.record_types = self._parse_types()
        self.record_source = self._parse_source()
        self.rights = self._parse_rights()
        self.record_info_link = self._parse_info_link()

    def _parse_id(self): #TODO:
        record_ids = []
        for id_root in self.root.findall(paths["RecordLegal_RecordID_Path"], namespace):
            record_id = SourceID(id_root)
            record_ids.append(record_id)

        return record_ids

    def _parse_types(self):
        record_types = []
        for type_root in self.root.findall(paths["RecordType_ID_Path"], namespace):
            record_type = SourceID(type_root)
            # record_type._parse_term(self.root, "RecordType_Term_Path", None)
            record_types.append(record_type)

        return record_types

    def _parse_source(self):
        source = self.root.find(paths["RecordLegal_Source_Path"], namespace).text
        return source

    def _parse_rights(self):
        rights = self.root.find(paths["RecordLegal_Rights_Path"], namespace)
        if rights is not None:
            return Rights(rights)
        else:
            return None

    def _parse_info_link(self):
        record_info_links = []
        for info_link in self.root.findall(paths["RecordLegal_RecordInfoLink_Path"], namespace):
            record_info_links.append(info_link.text)

        return record_info_links

    def __json_repr__(self):
        return {
            "recordID": self.record_ids,
            "recordType": self.record_types,
            "recordSource": self.record_source,
            "rights": self.rights,
            "recordInfoLink": self.record_info_link
        }