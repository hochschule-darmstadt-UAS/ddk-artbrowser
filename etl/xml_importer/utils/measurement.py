from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.parseLido import filter_none


class Measurement:
    def __init__(self, root):
        self.root = root
        self.displayName = ""
        self.parse()

    def parse(self):
        self.displayName = self._parse_displayName()

    def _parse_displayName(self):
        displayName = self.root.find(paths["Measurement_DisplayName_Path"], namespace)
        if displayName is not None:
            return displayName.text

        return ""

    def __json_repr__(self):
        json = {
            "displayName": self.displayName,
        }
        return filter_none(json)
