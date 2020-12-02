from xpaths import paths
namespace = {'lido': 'http://www.lido-schema.org'}


class Measurment():
    def __init__(self, measurments_sets):
        self.root = measurments_sets
        self.measurment = {
            "displaySize": "",
            "type": "",
            "unit": "",
            "value": "",
            "extend": "",
            "displayName": "",
            "shape": "",
            "format": "",
            "qualifier": "",
        }
        self.parse()

    def parse(self):
        self.measurment["displaySize"] = self.root[0].findall(paths["Artwork_Mesurments_DisplaySize_Path"], namespace)[0].text
        self.measurment["type"] = self.root[0].findall(paths["Artwork_Mesurments_Type_Path"], namespace)[0].text
        self.measurment["unit"] = self.root[0].findall(paths["Artwork_Mesurments_Unit_Path"], namespace)[0].text
        self.measurment["value"] = self.root[0].findall(paths["Artwork_Mesurments_Value_Path"], namespace)[0].text

        measurmentsets = []
        for measurments_set in self.root:
            measurmentset = measurments_set.findall('lido:displayObjectMeasurements', namespace)
            if len(measurmentset) > 0:
                measurmentsets.append(measurmentset[0].text)
            else:
                pass

            shape = measurments_set.findall(paths["Artwork_Mesurments_Shape_Path"], namespace)
            if len(shape) > 0:
                self.measurment["shape"] = shape[0].text
            else:
                pass

            format = measurments_set.findall(paths["Artwork_Mesurments_Format_Path"], namespace)
            if len(format) > 0:
                self.measurment["format"] = format[0].text
            else:
                pass

            qualifier = measurments_set.findall(paths["Artwork_Mesurments_Qualifier_Path"], namespace)
            if len(qualifier) > 0:
                self.measurment["qualifier"] = qualifier[0].text
            else:
                pass

        self.measurment["displaySize"] = measurmentsets[0]

        if len(measurmentsets) > 1:
            self.measurment["displayName"] = measurmentsets[1]
        else:
            pass

    def getmeasurment(self):
        return self.measurment


class Record:
    def __init__(self, recordLegal):
        self.root = recordLegal
        self.recordLegal = {
            "recordID": {
                "source": "",
                "id": ""
            },
            "recordType": {
                "id": "",
                "term": ""
            },
            "recordSource": "",
            "rights": {
                "type": {
                    "id": "",
                    "term": ""
                },
                "rightsHolder": {
                    "source": "",
                    "id": "",
                    "term": ""
                }
            },
            "recordInfoLink": ""
        }
        self.parse()

    def get_recordLegal(self):
        return self.recordLegal

    def parse(self):
        self.recordID = self.root.findall(paths["Artwork_RecordLegal_RecordID_Path"], namespace)[0]
        self.recordType = self.root.findall(paths["Artwork_RecordLegal_RecordType_Path"], namespace)[0]
        self.recordSource = self.root.findall(paths["Artwork_RecordLegal_RecordSource_Path"], namespace)[0]
        self.rights = self.root.findall(paths["Artwork_RecordLegal_Rights_Path"], namespace)[0]
        self.recordInfoLink = self.root.findall(paths["Artwork_RecordLegal_RecordInfoLink_Path"], namespace)[0]

        self.recordLegal["recordID"]["source"] = self.recordID.attrib.get('{http://www.lido-schema.org}source', namespace)
        self.recordLegal["recordID"]["id"] = self.recordID.text

        self.recordLegal["recordType"]["id"] = self.recordType.findall('lido:conceptID', namespace)[0].text
        self.recordLegal["recordType"]["term"] = self.recordType.findall('lido:term', namespace)[0].text

        self.recordLegal["recordSource"] = self.recordSource.findall('lido:legalBodyName/lido:appellationValue', namespace)[0].text

        self.recordLegal["rights"]["type"]["id"] = self.rights.findall('lido:rightsType/lido:conceptID', namespace)[0].text
        self.recordLegal["rights"]["type"]["term"] = self.rights.findall('lido:rightsType/lido:term', namespace)[0].text

        self.rightsHolder = self.rights.findall('lido:rightsHolder/lido:legalBodyID', namespace)
        if len(self.rightsHolder) > 0:
            self.recordLegal["rights"]["rightsHolder"]["source"] = self.rightsHolder[0].attrib.get('{http://www.lido-schema.org}source', namespace)
            self.recordLegal["rights"]["rightsHolder"]["id"] = self.rightsHolder[0].text
            self.recordLegal["rights"]["rightsHolder"]["term"] = self.rights.findall('lido:rightsHolder/lido:legalBodyName/lido:appellationValue', namespace)[0].text
        else:
            pass

        self.recordLegal["recordInfoLink"] = self.recordInfoLink.text

        return self.recordLegal


class Resource:
    def __init__(self, resourceLegal):
        self.root = resourceLegal
        self.resourceLegal = {
            "resourceID": {
                "id": ""
            },
            "resourceType": "",
            "rights": {
                "type": {
          "id": "",
          "term": ""
        },
                "rightsHolder": {
          "source": "",
          "id": "",
          "term": "Bildarchiv Foto Marburg"
        }
            },
            "resourceDateTaken": "",
             "linkResource": ""
         }
        self.parse()
        self.getresourceLegal()

    def parse(self):
        self.resourceID = self.root[0].findall(paths["Artwork_ResourceLegal_resourceID_Path"], namespace)[0]
        self.resourceType = self.root[0].findall(paths["Artwork_ResourceLegal_resourceType_Path"], namespace)[0]
        self.rights = self.root[0].findall(paths["Artwork_ResourceLegal_Rights_Path"], namespace)[0]
        self.resourceDateTaken = self.root[0].findall(paths["Artwork_ResourceLegal_ResourceDateTaken_Path"], namespace)
        self.linkResource =self.root[0].findall(paths["Artwork_ResourceLegal_LinkResource_Path"], namespace)[0]

        self.resourceLegal["resourceID"]["id"] = self.resourceID.text
        self.resourceLegal["resourceType"] = self.resourceType.text
        self.resourceLegal["rights"]["type"]["id"] = self.rights.findall('lido:rightsType/lido:conceptID', namespace)[0].text
        self.resourceLegal["rights"]["type"]["term"] = self.rights.findall('lido:rightsType/lido:term', namespace)[0].text

        self.rightsHolder = self.rights.findall('lido:rightsHolder/lido:legalBodyID', namespace)
        if len(self.rightsHolder) > 0:
            self.resourceLegal["rights"]["rightsHolder"]["source"] = self.rightsHolder[0].attrib.get('{http://www.lido-schema.org}source', namespace)
            self.resourceLegal["rights"]["rightsHolder"]["id"] = self.rightsHolder[0].text
            self.resourceLegal["rights"]["rightsHolder"]["term"] = self.rights.findall('lido:rightsHolder/lido:legalBodyName/lido:appellationValue', namespace)[0].text
        else:
            pass

        if len(self.resourceDateTaken) > 0:
            self.resourceLegal["resourceDateTaken"] = self.resourceDateTaken[0].text
        else:
            pass

        self.resourceLegal["linkResource"] = self.linkResource.text

    def getresourceLegal(self):
        return self.resourceLegal





