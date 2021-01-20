from etl.xml_importer.xpaths import namespace
from etl.xml_importer.utils.rights import Rights
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths
from etl.xml_importer.parseLido import filter_none


class RecordLegal:
    def __init__(self, root):
        self.root = root
        self._parse_id()
        self._parse_types()
        self._parse_source()
        self._parse_rights()
        self._parse_info_link()
        self.clear()

    def _parse_id(self):
        self.record_ids = []
        for id_root in self.root.findall(paths["RecordLegal_RecordID_Path"], namespace):
            record_id = SourceID(id_root)
            self.record_ids.append(record_id)

    def _parse_types(self):
        self.record_types = []
        for type_root in self.root.findall(paths["RecordType_ID_Path"], namespace):
            record_type = SourceID(type_root)
            # record_type._parse_term(self.root, "RecordType_Term_Path", None)
            self.record_types.append(record_type)

    def _parse_source(self):
        source_root = self.root.find(paths["RecordLegal_Source_Path"], namespace)
        if source_root is not None:
            self.record_source = source_root.text
        else:
            self.record_source = None

    def _parse_rights(self):
        rights = self.root.find(paths["RecordLegal_Rights_Path"], namespace)
        if rights is not None:
            self.rights = Rights(rights)
        else:
            self.rights = None

        del rights

    def _parse_info_link(self):
        self.record_info_links = []
        for info_link in self.root.findall(paths["RecordLegal_RecordInfoLink_Path"], namespace):
            self.record_info_links.append(info_link.text)

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "recordIDs": self.record_ids,
            "recordType": self.record_types,
            "recordSource": self.record_source,
            "rights": self.rights,
            "recordInfoLink": self.record_info_links
        }
        return filter_none(json)
