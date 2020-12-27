from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Iconography():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):##Todo:sanitize id
        id_root = self.root.find(paths["Icongraphy_Id_Path"], namespace)
        if id_root is not None:
            id = id_root.text.split('/')[-1]
            integer = id.find(')')
            if integer > 0:
                id = id[:integer+1]
            return id
        return ""
    #11H(Francis)344(+3) -->11H(Francis)
    #98B(Antiochus%20I)61 -->98B(Antiochus%20I)
    #98B(Nero)52 -->98B(Nero)
    #25H13 -->25H13
    #61B2(...)11(+51) -->61B2(...)11(+51)

    def parse(self):
        self.entity_type= 'Iconography'
        self.concepts = []
        self.name = self._parse_name()
        self.iconclass = self._parse_iconclass()

        for source_id in self.root.findall(paths["Icongraphy_Id_Path"], namespace):
            concept = SourceID(source_id)
            self.concepts.append(concept)

    def _parse_name(self):
        name_root = self.root.find(paths["Icongraphy_Name_Path"], namespace)
        if name_root is not None:
            return name_root.text
        else:
            return ""

    def _parse_iconclass(self):
        iconclass_root = self.root.find(paths["Icongraphy_Iconclass_Path"], namespace)
        if iconclass_root is not None:
            return iconclass_root.text
        else:
            return ""