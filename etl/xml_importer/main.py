import xml.etree.ElementTree as xml
import json
import copy

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
#icongraphy und genre dict muss in forl ein dict definiert werden
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

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:titleWrap/lido:titleSet/lido:appellationValue', self.namespace)):
            if (element.attrib.get('{http://www.lido-schema.org}pref') == 'preferred'):
                artworks[i]["name"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet[1]/lido:displayObjectMeasurements', self.namespace)):
            artworks[i]["measurements"][0]["displayName"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet[1]/lido:objectMeasurements/lido:measurementsSet/lido:measurementType', self.namespace)):
            artworks[i]["measurements"][0]["measurementsType"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet[1]/lido:objectMeasurements/lido:measurementsSet/lido:measurementUnit', self.namespace)):
            artworks[i]["measurements"][0]["unit"] = element.text

        for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet[1]/lido:objectMeasurements/lido:measurementsSet/lido:measurementValue',self.namespace)):
            artworks[i]["measurements"][0]["value"] = element.text

##Frage ob wir überhaupt displayName, shape, format, qualifier brauchen
        #for i, element in enumerate(self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:objectMeasurementsWrap/lido:objectMeasurementsSet/*',self.namespace)):

    #Es gibt zwei Stelle für RecordLegal.welche muss deefiniert werden







    def location(self):
        locations = []
        for element in self.root.findall('lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:repositoryWrap/lido:repositorySet[1]/lido:repositoryName/lido:legalBodyName/lido:appellationValue', self.namespace):
           l = location.copy()
           l['id'] = element.text
           locations.append(l)
        #print(locations)

if __name__ == '__main__':
    data = 'merged.xml'
    artwork = Artwork(data)
    artwork.location()


with open("artworks.json", "w", encoding="utf-8") as f:
    json.dump(artworks, f, ensure_ascii=False, indent=4)




