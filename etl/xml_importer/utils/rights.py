from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.parseLido import filter_none


class Rights:

    def __init__(self, root, ):
        self.root = root
        self.types = self._parse_types()
        self.holders = self._parse_holders()

    def _parse_types(self):
        rights_type = self.root.find(paths['Rights_Type_Path'], namespace)
        if rights_type is not None:
            return SourceID(rights_type)
        else:
            return None

    def _parse_holders(self):
        rights_holder = self.root.find(paths['Rights_Holder_Path'], namespace)
        if rights_holder is not None:
            return SourceID(rights_holder, term_path='lido:legalBodyName/lido:appellationValue')
        else:
            return None

    def __json_repr__(self):
        json = {
            "rightsType": self.types,
            "rightsHolder": self.holders,
        }
        return filter_none(json)
