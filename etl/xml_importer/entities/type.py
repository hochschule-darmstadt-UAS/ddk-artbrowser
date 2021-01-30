from etl.xml_importer.parseLido import get_id_by_prio, sanitize_id, sanitize, filter_none
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import namespace, paths
from etl.xml_importer.encoding import JSONEncodable

import logging


class Type(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = "type"
        self._parse_id()

        self.label = ""
        self.alt_labels = []
        self.source_ids = []

        self.count = 1
        self.rank = 0

        logging.info('A type was parsed from xml file complete.')

    def _parse_id(self):
        all_type_ids = self.root.findall(paths["Type_ID_Path"], namespace)
        if len(all_type_ids) > 0:
            id = get_id_by_prio(all_type_ids)
            self.id = id
        else:
            self._parse_label()
            self.id = self.label

        self.id = sanitize_id(self.id)
        # add entity type as id prefix to ensure uniqueness
        self.id = self.entity_type + "-" + self.id

    def parse(self):
        self._parse_label()
        self._parse_alt_labels()
        self._parse_source_ids()

    def _parse_label(self):
        # here we use the xpath(...) function instead of find/finall so that we can use the xpath 'not' feature
        # (see 'Type_Label_Path' in xpaths.py). This seems not to be supported by the find/findall function.
        label_root = self.root.xpath(paths["Type_Label_Path"], namespaces=namespace)
        if len(label_root) > 0:
            self.label = sanitize(label_root[0].text)
        else:
            self.label = ""

    def _parse_alt_labels(self):
        self.alt_labels = []
        for alt_label_root in self.root.findall(paths["Type_AltLabel_Path"], namespace):
            self.alt_labels.append(alt_label_root.text)

    def _parse_source_ids(self):
        self.source_ids = []
        for source_id_root in self.root.findall(paths["Type_ID_Path"], namespace):
            source_id = SourceID(source_id_root)
            self.source_ids.append(source_id)

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "altLabels": self.alt_labels,
            "sourceIDs": self.source_ids,
            "count": self.count,
            "rank": self.rank,
        }
        return filter_none(json)
