from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.parseLido import filter_none


class Measurement:
    def __init__(self, root):
        self.root = root
        self.displayName = ""
        self.parse()
        self.clear()

    def parse(self):
        self._parse_displayName()

    def _parse_displayName(self):
        displayName = self.root.find(paths["Measurement_DisplayName_Path"], namespace)
        if displayName is not None:
            self.displayName = displayName.text
        else:
            self.displayName = ""

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "displayName": self.displayName,
        }
        return filter_none(json)
