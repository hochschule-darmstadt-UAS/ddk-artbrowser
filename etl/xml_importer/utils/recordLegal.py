#TODO: noch ueberarbeiten

class RecordLegal:
    def __init__(self, recordIDs, recordTypes,
                 recordSource, rights,
                 recordInfoLink
                 #recordLegal
                 ):
        #self.root = recordLegal
        self.recordIDs = recordIDs
        self.recordTypes = recordTypes
        self.recordSource = recordSource
        self.rights = rights
        self.recordInfoLink = recordInfoLink
        self.parse()

    def get_recordLegal(self):
        return self.recordLegal

    def parse(self):
       # self.recordID = self.root.findall(paths["Artwork_RecordLegal_RecordID_Path"], namespace)[0]
       # self.recordType = self.root.findall(paths["Artwork_RecordLegal_RecordType_Path"], namespace)[0]
       # self.recordSource = self.root.findall(paths["Artwork_RecordLegal_RecordSource_Path"], namespace)[0]
       #self.rights = self.root.findall(paths["Artwork_RecordLegal_Rights_Path"], namespace)[0]
        #self.recordInfoLink = self.root.findall(paths["Artwork_RecordLegal_RecordInfoLink_Path"], namespace)[0]

     #   self.recordLegal["recordID"]["source"] = self.recordID.attrib.get('{http://www.lido-schema.org}source', namespace)
        self.recordLegal["recordID"]["id"] = self.recordID.text

       # self.recordLegal["recordType"]["id"] = self.recordType.findall('lido:conceptID', namespace)[0].text
       # self.recordLegal["recordType"]["term"] = self.recordType.findall('lido:term', namespace)[0].text

      #  self.recordLegal["recordSource"] = self.recordSource.findall('lido:legalBodyName/lido:appellationValue', namespace)[0].text

       # self.recordLegal["rights"]["type"]["id"] = self.rights.findall('lido:rightsType/lido:conceptID', namespace)[0].text
        #self.recordLegal["rights"]["type"]["term"] = self.rights.findall('lido:rightsType/lido:term', namespace)[0].text

        #self.rightsHolder = self.rights.findall('lido:rightsHolder/lido:legalBodyID', namespace)
       # if len(self.rightsHolder) > 0:
          #  self.recordLegal["rights"]["rightsHolder"]["source"] = self.rightsHolder[0].attrib.get('{http://www.lido-schema.org}source', namespace)
          #  self.recordLegal["rights"]["rightsHolder"]["id"] = self.rightsHolder[0].text
          #  self.recordLegal["rights"]["rightsHolder"]["term"] = self.rights.findall('lido:rightsHolder/lido:legalBodyName/lido:appellationValue', namespace)[0].text
       # else:
          #  pass

        self.recordLegal["recordInfoLink"] = self.recordInfoLink.text

        return self.recordLegal

#recordIDs SourceID[]
#recordTypes SourceID[]
#recordSource string
#rights Rights
#recordInfoLink string[]