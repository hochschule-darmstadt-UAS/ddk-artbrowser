from etl.xml_importer.parseLido import get_id_by_prio, sanitize_id, sanitize
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import namespace, paths
from etl.xml_importer.encoding import JSONEncodable


class Type(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = "type"
        self.id = self._parse_id()

        self.label = ""
        self.alt_labels = []
        self.source_ids = []

    def _parse_id(self):
        all_type_ids = self.root.findall(paths["Type_ID_Path"], namespace)
        id = get_id_by_prio(all_type_ids)

        return sanitize_id(id)

    def parse(self):
        self.label = self._parse_label()
        self.alt_labels = self._parse_alt_labels()
        self.source_ids = self._parse_source_ids()

    def _parse_label(self):
        # here we use the xpath(...) function instead of find/finall so that we can use the xpath 'not' feature
        # (see 'Type_Label_Path' in xpaths.py). This seems not to be supported by the find/findall function.
        label_root = self.root.xpath(paths["Type_Label_Path"], namespaces=namespace)
        if len(label_root) > 0:
            return sanitize(label_root[0].text)
        else:
            return ""

    def _parse_alt_labels(self):
        alt_labels = []
        for alt_label_root in self.root.findall(paths["Type_AltLabel_Path"], namespace):
            alt_labels.append(alt_label_root.text)

        return alt_labels

    def _parse_source_ids(self):
        source_ids = []
        for source_id_root in self.root.findall(paths["Type_ID_Path"], namespace):
            source_id = SourceID(source_id_root)
            source_ids.append(source_id)

        return source_ids

    def __json_repr__(self):
        return {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "altLabels": self.alt_labels,
            "sourceID": self.source_ids,
        }
