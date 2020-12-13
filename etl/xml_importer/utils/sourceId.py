from etl.xml_importer.xpaths import namespace, paths


class SourceID():

    def __init__(self, current_id):
        self.id = current_id

    def _parse_source(self):
        tmp = self.id.split('/')[-1]
        #TODO: source als Attribute heraulesen, damit tmp-Variable nicht gebraucht wird
        self.source = self.id.split(tmp)[0]

    def _parse_term(self, path, pathName, pathAltname):
        self.name = path.find(paths[pathName], namespace).text
        self.altname = []

        for tmp in path.findall(paths[pathAltname], namespace):
            self.altname.append(tmp.text)