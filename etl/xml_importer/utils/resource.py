#TODO: noch ueberarbeiten

class Resource:
    def __init__(self, root):
        self.root = root
        self.resourceIDs = self._parse_resourceID()
        self.resourceType = self._parse_resourceType()
        self.rights = self._parse_rights()
        self.resourceDateTaken = self._parse_resourceDateTaken()
        self.linkResource = self._parse_linkResource()
        self.photographer = self._parse_photographer()

    def _parse_resourceID(self):
        pass

    def _parse_resourceType(self):
        pass

    def _parse_rights(self):
        pass

    def _parse_resourceDateTaken(self):
        pass

    def _parse_linkResource(self):
        pass

    def _parse_photographer(self):
        pass


    def parse(self):
       # self.resourceID = self.root[0].findall(paths["Artwork_ResourceLegal_resourceID_Path"], namespace)[0]
       # self.resourceType = self.root[0].findall(paths["Artwork_ResourceLegal_resourceType_Path"], namespace)[0]
        #self.rights = self.root[0].findall(paths["Artwork_ResourceLegal_Rights_Path"], namespace)[0]
       # self.resourceDateTaken = self.root[0].findall(paths["Artwork_ResourceLegal_ResourceDateTaken_Path"], namespace)
        #self.linkResource =self.root[0].findall(paths["Artwork_ResourceLegal_LinkResource_Path"], namespace)[0]

        self.resourceLegal["resourceID"]["id"] = self.resourceID.text
        self.resourceLegal["resourceType"] = self.resourceType.text
        #self.resourceLegal["rights"]["type"]["id"] = self.rights.findall('lido:rightsType/lido:conceptID', namespace)[0].text
       # self.resourceLegal["rights"]["type"]["term"] = self.rights.findall('lido:rightsType/lido:term', namespace)[0].text

        #self.rightsHolder = self.rights.findall('lido:rightsHolder/lido:legalBodyID', namespace)
        #if len(self.rightsHolder) > 0:
        #    self.resourceLegal["rights"]["rightsHolder"]["source"] = self.rightsHolder[0].attrib.get('{http://www.lido-schema.org}source', namespace)
        #    self.resourceLegal["rights"]["rightsHolder"]["id"] = self.rightsHolder[0].text
        #    self.resourceLegal["rights"]["rightsHolder"]["term"] = self.rights.findall('lido:rightsHolder/lido:legalBodyName/lido:appellationValue', namespace)[0].text
        #else:
         #   pass

        #if len(self.resourceDateTaken) > 0:
        #    self.resourceLegal["resourceDateTaken"] = self.resourceDateTaken[0].text
       # else:
         #   pass

        self.resourceLegal["linkResource"] = self.linkResource.text

    def getresourceLegal(self):
        return self.resourceLegal

#resourceIDs SourceID[]
#resourceType string
#rights Rights
#photographer string
#dateTaken string
#linkResource string