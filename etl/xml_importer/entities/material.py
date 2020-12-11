class Material():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()
        self.type = 'type'
        self.conceptID = self._parse_conceptID()
        self.name = self._parse_name()

    def _parse_id(self):
        pass

    def _parse_conceptID(self):
        pass

    def _parse_name(self):
        pass

#id
#entityType string
#conceptID SourceID[]
#name string
#altNames string[] 2