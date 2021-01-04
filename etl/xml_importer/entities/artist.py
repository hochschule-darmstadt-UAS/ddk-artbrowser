from etl.xml_importer.parseLido import get_id_by_prio, sanitize_id, filter_none
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace

from etl.xml_importer.encoding import JSONEncodable


class Artist(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'artist'
        self.id = self._parse_id()

        self.label = ""
        self.source_ids = []
        self.birth = ""
        self.death = ""

    def _parse_id(self):
        all_artist_ids = self.root.findall(paths["Artist_ID_Path"], namespace)
        id = get_id_by_prio(all_artist_ids)
        return sanitize_id(id)

    def parse(self):
        self.source_ids = self._parse_source_ids()
        self.label = self._parse_label()
        self.birth = self._parse_birth()
        self.death = self._parse_death()

    def _parse_label(self):
        label = self.root.find(paths["Artist_Name_Path"], namespace).text
        return label.strip()

    def _parse_source_ids(self):
        source_ids = []
        for source_id_root in self.root.findall(paths["Artist_ID_Path"], namespace):
            source_id = SourceID(source_id_root)
            source_ids.append(source_id)

        return source_ids

    def _parse_birth(self):
        birthDate = self.root.find(paths["Artist_Birth_Path"], namespace)
        if birthDate != None:  #Kann ein Artist kein Geburtsdatum haben
            return birthDate.text
        else:
            return ''

    def _parse_death(self):
        deathDate = self.root.find(paths["Artist_Death_Path"], namespace)
        if deathDate != None:
            return deathDate.text
        else:
            return ''

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "sourceID": self.source_ids,
            "dateOfBirth": self.birth,
            "dateOfDeath": self.death,
        }
        return filter_none(json)
