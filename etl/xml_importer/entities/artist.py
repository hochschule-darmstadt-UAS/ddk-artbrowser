from etl.xml_importer.parseLido import get_id_by_prio, sanitize_id, filter_none
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace

from etl.xml_importer.encoding import JSONEncodable


class Artist(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'artist'
        self._parse_id()

        self.label = ""
        self.source_ids = []
        self.birth = ""
        self.death = ""

    def _parse_id(self):
        all_artist_ids = self.root.findall(paths["Artist_ID_Path"], namespace)
        id = get_id_by_prio(all_artist_ids)
        self.id = sanitize_id(id)

    def parse(self):
        self._parse_source_ids()
        self._parse_label()
        self._parse_birth()
        self._parse_death()

    def _parse_label(self):
        label_root = self.root.find(paths["Artist_Name_Path"], namespace)
        if label_root is not None:
            label = label_root.text
            self.label = label.strip()
        else:
            self.label = None

    def _parse_source_ids(self):
        for source_id_root in self.root.findall(paths["Artist_ID_Path"], namespace):
            source_id = SourceID(source_id_root)
            self.source_ids.append(source_id)

    def _parse_birth(self):
        birth_date_root = self.root.find(paths["Artist_Birth_Path"], namespace)
        if birth_date_root is not None:  #Kann ein Artist kein Geburtsdatum haben
            self.birth = birth_date_root.text
        else:
            self.birth = ''

    def _parse_death(self):
        death_date_root = self.root.find(paths["Artist_Death_Path"], namespace)
        if death_date_root is not None:
            self.death = death_date_root.text
        else:
            self.death = ''

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "sourceIDs": self.source_ids,
            "dateOfBirth": self.birth,
            "dateOfDeath": self.death,
        }
        return filter_none(json)
