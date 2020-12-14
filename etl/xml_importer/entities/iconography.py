from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Iconography():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):##Todo:sanitize id
        id = self.root.find(paths["Icongraphy_Id_Path"], namespace).text.split('/')[-1]
        integer = id.find(')')
        if integer > 0:
            id = id[:integer+1]
        return id
    #11H(Francis)344(+3) -->11H(Francis)
    #98B(Antiochus%20I)61 -->98B(Antiochus%20I)
    #98B(Nero)52 -->98B(Nero)
    #25H13 -->25H13
    #61B2(...)11(+51) -->61B2(...)11(+51)

    def parse(self):
        self.entity_type= 'Iconography'
        self.concepts = []
        self.name = self.root.find(paths["Icongraphy_Name_Path"], namespace).text

        for source_id in self.root.findall(paths["Icongraphy_Id_Path"], namespace):
            concept = SourceID(source_id.text)
            concept._parse_source()
            concept._parse_term(self.root, "Icongraphy_Name_Path", "Icongraphy_Altname_Path")
            self.concepts.append(concept)

#id
#entityType string
#conceptID SourceID[]
#name string
#altNames string[] 2