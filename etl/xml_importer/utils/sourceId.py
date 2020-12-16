from etl.xml_importer.xpaths import namespace, paths


class SourceID():

    def __init__(self, root):
        self.id = root.text
        self.root = root

    def _parse_source(self):
        #print(self.root.get('lido:recordID'))
        #print(self.root.attrib.get("lido:recordID"))

        tmp = self.id.split('/')[-1]
        #TODO: source als Attribute heraulesen, damit tmp-Variable nicht gebraucht wird
        self.source = self.id.split(tmp)[0]

    def _parse_term(self, path, pathName, pathAltname):
        self.name = path.find(paths[pathName], namespace).text
        self.altnames = []

        if pathAltname != "0":
            for tmp in path.findall(paths[pathAltname], namespace):
                self.altnames.append(tmp.text)