import xml.etree.ElementTree as xml
import json
import copy
from xpaths import paths
import utils

namespace = {'lido': 'http://www.lido-schema.org'}

class LidoObject():
    def __init__(self, root):
        self.root = root
        self.artwork = None
        self.parse()


    def parse(self):
        self.artwork = Artwork(self.root)


class Artwork:
    def __init__(self, root):
        self.root = root
        self.id = ""
        self.type = "artwork"
        self.name = ""
        self.measurements = []
        self.recordLegal = {}
        self.resourceLegal = {}
        self.types = {}
        self.genres = []
        self.location = ""
        self.artists = []
        self.iconographies = []
        self.inscription = ""
        self.altName = []
        self.count = ""
        self.rank = ""

        self.parse()
        #self.count()
        #self.rank()

    def parse(self):
        self._parse_id()
        self._parse_name()
        self._parse_measurements()
        self._parse_recordLegal()
        self._parse_resourceLegal()
        #self._parse_types()
        #self._parse_genres()
        #self._parse_location()
        #self._parse_artists()
        #self._parse_iconographies()
        #self._parse_inscription()
        #self._parse_altName()

    def _parse_id(self):
        id_list = self.root.findall(paths["Artwork_Id_Path"], namespace)
        for id in id_list:
            self.id = id.text.replace("/", "-").replace(",", "-")

    def _parse_name(self):
        name_list = self.root.findall(paths["Artwork_Name_Path"], namespace)
        for name in name_list:
            self.name = name.text

    def _parse_measurements(self):
        measurments_sets = self.root.findall(paths["Artwork_Measurements_Path"], namespace)
        print(len(measurments_sets))
        if (len(measurments_sets) > 0):
            self.measurements.append(utils.Measurment(measurments_sets))


    def _parse_recordLegal(self):
        recordLegal_List = self.root.findall(paths["Artwork_RecordLegal_Path"], namespace)
        #print(recordLegal_List)
        for recordLegal in recordLegal_List:
            self.recordLegal = utils.Record(recordLegal)

    def _parse_resourceLegal(self):
        resourceLegal_List = self.root.findall(paths["Artwork_ResourceLegal_Path"], namespace)
        for resourceLegal in resourceLegal_List:
            utils.Resource(resourceLegal)

    def __json_repr__(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            #'measurements': self.measurements
            'recordLegal': self.recordLegal




            }
    #def _parse_types(self):














'''

location = {
    "id": "",
    "entityType": "",
    "name": "",
    "altNames": [""],
    "inventoryNumber": "",
    "placeID": {
      "source": "",
      "id": "",
      "term": ""
    },
    "placeName": "",
    "placeAltNames": [""],
    "count": "",
    "rank": ""
  }
material = {
    "id": "",
    "entityType": "",
    "conceptID": [
      {
        "source": "",
        "id": ""
      },
      {
        "source": "",
        "id": ""
      }
    ],
    "name": "",
    "altNames": [""],
    "count": "",
    "rank": ""
}
artist = {
    "id": "",
    "entityType": "",
    "actorId": [
      {
        "source": "",
        "id": ""
      },
      {
        "source": "",
        "id": ""
      }
    ],
    "name": "",
    "altNames": [""],
    "nationality": "",
    "birth": "",
    "death": "",
    "gender": "",
    "roles": [""],
    "count": "",
    "rank": ""
}
type = {
    "id": "",
    "entityType": "",
    "name": "",
    "altNames": [""],
    "conceptID": [
      {
        "source": "",
        "id": "",
        "term": ""
      },
      {
        "source": "",
        "id": "",
        "term": ""
      }
    ],
    "count": "",
    "rank": ""
  }
#icongraphy und genre dict muss in form eines dict definiert werden
icongraphy = {"1":
    {
    "id": "",
    "entityType": "",
    "conceptID": {
      "source": "",
      "id": ""
    },
    "name": "",
    "altNames": [""],
    "count": "",
    "rank": ""
  }, "2":
  {
    "id": "",
    "entityType": "",
    "conceptID": {
      "source": "",
      "id": ""
    },
    "name": "",
    "altNames": [""],
    "count": "",
    "rank": ""
  }
}
genre = { "1":
    {
    "id": "",
    "entityType": "",
    "classificationType": "",
    "name": "",
    "conceptID": [
      {
        "source": "h",
        "id": "",
        "term": ""
      },
      {
        "source": "",
        "id": "",
        "term": ""
      }
    ],
    "count": "",
    "rank": ""
  }, "2":
  {
    "id": "",
    "entityType": "",
    "classificationType": "",
    "name": "",
    "count": "",
    "rank": ""
  }, "3":
  {
    "id": "",
    "entityType": "",
    "classificationType": "",
    "name": "",
    "count": "",
    "rank": ""
  }
}
artwork = {
    "id": "",
    "entityType": "artwork",
    "name": "",
    "measurements": [
      {
        "displayName": "",
        "measurementsType": "",
        "unit": "",
        "value": "",
        "extend": "gesamt"
      },
      {
        "displayName": ""
      },
      {
        "shape": ""
      },
      {
        "format": ""
      },
      {
        "qualifier": ""
      }
    ],
    "recordLegal": {
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
        "rightsType": {
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
    },
    "resources": [
      {
        "resourceID": {
          "id": ""
        },
        "resourceType": "",
        "rights": {
          "rightsType": {
            "id": "",
            "term": ""
          },
          "rightsHolder": {
            "source": "",
            "id": "",
            "term": ""
          }
        },
        "dateTaken": "",
        "linkResource": ""
      }
    ],
    "types": [""],
    "genres": [""],
    "location": "",
    "artists": [""],
    "iconographies": [""],
    "inscriptions": [""],
    "altName": [""],
    "count": "",
    "rank": ""
  }


artworks = []

class Artwork:
    def __init__(self, data):
        self.root = xml.parse(data).getroot()
        self.namespace = {'lido': 'http://www.lido-schema.org'}

        for i, element in enumerate(self.root.findall('lido:lido/lido:lidoRecID', self.namespace)):
            cp = copy.deepcopy(artwork)
            artworks.append(cp)
            id = element.text.replace("/", "-").replace(",", "-")
            artworks[i]["id"] = id

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue[@lido:pref="preferred"][1]', self.namespace)):
            print(element.text)
            artworks[i]["name"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet[1]/lido:displayObjectMeasurements', self.namespace)):
            artworks[i]["measurements"][0]["displayName"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet[1]/lido:objectMeasurements/lido:measurementsSet/lido:measurementType', self.namespace)):
            artworks[i]["measurements"][0]["measurementsType"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet[1]/lido:objectMeasurements/lido:measurementsSet/lido:measurementUnit', self.namespace)):
            artworks[i]["measurements"][0]["unit"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet[1]/lido:objectMeasurements/lido:measurementsSet/lido:measurementValue',self.namespace)):
            artworks[i]["measurements"][0]["value"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectRelationWrap/lido:relatedWorksWrap/lido:relatedWorkSet/lido:relatedWork/lido:object/lido:objectID', self.namespace)):
            source = element.attrib.get('{http://www.lido-schema.org}source')
            id = element.attrib.get('{http://www.lido-schema.org}type')
            artworks[i]["recordLegal"]["recordID"]["source"] = element.text




##Frage ob wir überhaupt displayName, shape, format, qualifier brauchen
        #for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet/*',self.namespace)):

    #Es gibt zwei Stelle für RecordLegal.welche muss deefiniert werden



    def location(self):
        locations = []
        for element in self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:repositoryWrap/lido:repositorySet[1]/lido:repositoryName/lido:legalBodyName/lido:appellationValue', self.namespace):
           l = location.copy()
           l['id'] = element.text
           locations.append(l)


if __name__ == '__main__':
    data = 'merged.xml'
    artwork = Artwork(data)
    artwork.location()


with open("artworks.json", "w", encoding="utf-8") as f:
    json.dump(artworks, f, ensure_ascii=False, indent=4)

'''


