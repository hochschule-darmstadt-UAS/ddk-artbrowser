from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.parseLido import sanitize_id, sanitize, filter_none
from etl.xml_importer.encoding import JSONEncodable


class Iconography(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'iconography'
        self._parse_id()

        self.label = ""
        self.iconclass = ""
        self.source_ids = []

    def _parse_id(self):
        # 11H(Francis)344(+3) -->11H(Francis)
        # 98B(Antiochus%20I)61 -->98B(Antiochus%20I)
        # 98B(Nero)52 -->98B(Nero)
        # 25H13 -->25H13
        # 61B2(...)11(+51) -->61B2(...)11(+51)

        id_root = self.root.find(paths["Iconography_Id_Path"], namespace)
        if id_root is not None:
            id = id_root.text.split('/')[-1]
            self.id = id
        else:
            self.id = ""

    def parse(self):
        self._parse_source_ids()
        self._parse_label()
        self._parse_iconclass()

    def _parse_label(self):
        label_root = self.root.find(paths["Iconography_Label_Path"], namespace)
        if label_root is not None:
            self.label = sanitize(label_root.text)
        else:
            self.label = ""

    def _parse_iconclass(self):
        iconclass_root = self.root.find(paths["Iconography_Iconclass_Path"], namespace)
        if iconclass_root is not None:
            self.iconclass = iconclass_root.text
        else:
            self.iconclass = ""

    def _parse_source_ids(self):
        self.source_ids = []
        for source_id in self.root.findall(paths["Iconography_Id_Path"], namespace):
            concept = SourceID(source_id)
            self.source_ids.append(concept)

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "sourceIDs": self.source_ids,
        }
        return filter_none(json)
