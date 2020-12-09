from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.xpaths import namespace, paths


class SourceID():

    def __init__(self, sourceID):
        self.root = sourceID
        self.source = self._parse_source()
        self.id = self._parse_id()
        self.term = self._parse_term()

    def _parse_source(self):
        sourse = self.root.findall(paths["SourceID_Source_Path"], namespace)
        if len(sourse) > 0:
            source_name = sourse[0].attrib.get('{http://www.lido-schema.org}source')
        else:
            source_name = ''

        #print(source_name)
        return source_name

    def _parse_id(self):
        sourse = self.root.findall(paths["SourceID_Source_Path"], namespace)
        if len(sourse) > 0:
            id = get_id_by_prio(sourse)
        else:
            id = ''
        #print(id)
        return id

    def _parse_term(self):
        sourse = self.root.findall(paths["SourceID_Term_Path"], namespace)
        if len(sourse) > 0:
            term= sourse[0].text
        else:
            term = ''
        #print(term)
        return term

#source string
#id string
#term string