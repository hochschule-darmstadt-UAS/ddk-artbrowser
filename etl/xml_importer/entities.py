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
        self.artwork = Artwork(self.root)._get_Artwork()


class Artwork():
    def __init__(self, root):
        self.root = root
        self.artwork = {
            "id": None,
            "type": "artwork",
            "name": None,
            "measurements": [],
            "recordLegal": None,
            "resourceLegal": None,
            "types": None,
            "genres": [],
            "location": None,
            "artists": [],
            "iconographies": [],
            "inscription": None,
            "altName": [],
            "count": None,
            "rank": None,
        }
        self.parse()

    def parse(self):
        self._parse_id()
        self._parse_name()
        self._parse_measurements()
        self._parse_recordLegal()
        self._parse_resourceLegal()
        self._parse_types()
        self._parse_genres()
        self._parse_location()
        self._parse_artists()
        self._parse_iconographies()
        self._parse_inscription()
        self._parse_altName()
        self._get_Artwork()

    def _parse_id(self):
        id_list = self.root.findall(paths["Artwork_Id_Path"], namespace)
        for id in id_list:
            self.artwork["id"] = id.text.replace("/", "-").replace(",", "-")

    def _parse_name(self):
        name_list = self.root.findall(paths["Artwork_Name_Path"], namespace)
        for name in name_list:
            self.artwork["name"] = name.text

    def _parse_measurements(self):
        measurments_sets = self.root.findall(paths["Artwork_Measurements_Path"], namespace)
        #print(len(measurments_sets))
        if (len(measurments_sets) > 0):
            self.artwork["measurements"].append(utils.Measurment(measurments_sets).getmeasurment())
        else:
            pass

    def _parse_recordLegal(self):
        recordLegal_List = self.root.findall(paths["Artwork_RecordLegal_Path"], namespace)
        for recordLegal in recordLegal_List:
            self.artwork["recordLegal"] = utils.Record(recordLegal).get_recordLegal()

    def _parse_resourceLegal(self):
        resourceLegal_List = self.root.findall(paths["Artwork_ResourceLegal_Path"], namespace)
        if (len(resourceLegal_List) > 0):
            self.artwork["resourceLegal"] = utils.Resource(resourceLegal_List).getresourceLegal()

    def _parse_types(self):
        Artwork_Types = self.root.findall(paths["Artwork_Type_Path"], namespace)
        Types = []
        for Artwork_Type in Artwork_Types:
            type = Artwork_Type.text.split('/')[-1]
            Types.append(type)
        self.artwork["types"] = Types

    def _parse_genres(self):
        Artwork_Genres = self.root.findall(paths["Artwork_Genres_Path"], namespace)
        Genres = []
        for Artwork_Genre in Artwork_Genres:
            genre = Artwork_Genre.text.split('/')[-1]
            Genres.append(genre)
        self.artwork["genres"] = Genres

    def _parse_location(self):
        location = self.root.findall(paths["Artwork_Location_Path"], namespace)[0]
        self.artwork["location"] = location.text

    def _parse_artists(self):
        #jede Actor in lido_Object finden
        Artwork_Artists = self.root.findall(paths["Artwork_Artists_Path"], namespace)
        Artists = []
        for actor in Artwork_Artists:
            #für jede Actor find alle Actor_Ids
            ids = actor.findall('lido:actorInRole/lido:actor/lido:actorID', namespace)
            for id in ids:
                if 'getty' in id.text:
                    #print(id.text)
                    Artists.append(id.text.split('/')[-1])
                    break
                elif 'gnd' in id.text:
                    Artists.append(id.text.split('/')[-1])
                    break
                elif 'term' in id.text:
                    Artists.append(id.text.split('/')[-1])
                    break
                else:
                    pass
        self.artwork["artists"] = Artists

    def _parse_iconographies(self):
        iconographies_List = self.root.findall(paths["Artwork_Iconographies_Path"], namespace)
        iconographies = []
        for element in iconographies_List:
            iconographies.append(element.text.split('/')[-1])
        self.artwork["iconographies"] = iconographies

    def _parse_inscription(self):
        inscription_List = self.root.findall(paths["Artwork_Inscription_Path"], namespace)
        if len(inscription_List) > 0:
            self.artwork["inscription"] = inscription_List[0].text
        else:
            pass

    def _parse_altName(self):
        altenames_List = self.root.findall(paths["Artwork_Altename_Path"], namespace)
        altenames = []
        if len(altenames_List) > 0:
            for altename in  altenames_List:
                altenames.append(altename.text)
        else:
            pass
        self.artwork["altName"] = altenames

    def _get_Artwork(self):
        return self.artwork
