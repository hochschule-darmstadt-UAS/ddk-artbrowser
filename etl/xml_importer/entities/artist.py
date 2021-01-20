from etl.xml_importer.parseLido import get_id_by_prio, sanitize_id, filter_none
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace

from etl.xml_importer.encoding import JSONEncodable


class Artist(JSONEncodable):

    def __init__(self, root):
        self.root = root
        self.entity_type = 'artist'
        self.label = ""
        self.alt_labels = []

        self._parse_id()

        self.source_ids = []
        self.nationality = ""
        self.birth = ""
        self.death = ""
        self.evidenceFirst = ""
        self.evidenceLast = ""
        self.gender = ""
        self.roles = ""

        self.count = 1
        self.rank = 0

    def _parse_id(self):
        """
        Parses the id. If no id is present it parses the label and uses the label as id. If no label is present
        it parses the alt_labels and uses the first alt_label as id.
        """
        id = None
        all_artist_ids = self.root.findall(paths["Artist_ID_Path"], namespace)

        if len(all_artist_ids) > 0:
            id = get_id_by_prio(all_artist_ids)
        else:
            self._parse_label()
            if self.label:
                id = self.label
            # if label is also None, use the first alt label
            else:
                self._parse_alt_labels()
                if len(self.alt_labels) > 0:
                    id = self.alt_labels[0]

        if id is not None:
            # add entity type as id prefix to ensure uniqueness
            id = sanitize_id(id)
            self.id = self.entity_type + "-" + id
        else:
            self.id = None

    def parse(self):
        self._parse_source_ids()
        self._parse_label()
        self._parse_alt_labels()
        self._nationality()
        self._parse_birth()
        self._parse_death()
        self._parse_evidenceFirst()
        self._parse_evidenceLast()
        self._parse_gender()
        self._parse_roles()

    def _parse_label(self):
        label_root = self.root.find(paths["Artist_Name_Path"], namespace)
        if label_root is not None:
            label = label_root.text
            self.label = label.strip()
        else:
            self.label = None

    def _parse_alt_labels(self):
        self.alt_labels = []
        alt_label_roots = self.root.findall(paths["Artist_Altname_Path"], namespace)
        for root in alt_label_roots:
            self.alt_labels.append(root.text)

    def _nationality(self):
        nationality_root = self.root.find(paths["Artist_Nationality_Path"], namespace)
        if nationality_root is not None:
            self.death = nationality_root.text
        else:
            self.death = None

    def _parse_source_ids(self):
        for source_id_root in self.root.findall(paths["Artist_ID_Path"], namespace):
            source_id = SourceID(source_id_root)
            self.source_ids.append(source_id)

    def _parse_birth(self):
        birth_date_root = self.root.find(paths["Artist_Birth_Path"], namespace)
        if birth_date_root is not None:  #Kann ein Artist kein Geburtsdatum haben
            self.birth = birth_date_root.text
        else:
            self.birth = None

    def _parse_death(self):
        death_date_root = self.root.find(paths["Artist_Death_Path"], namespace)
        if death_date_root is not None:
            self.death = death_date_root.text
        else:
            self.death = None

    def _parse_evidenceFirst(self):
        evidenceFirst_root = self.root.find(paths["Artist_EvidenceFirst_Path"], namespace)
        if evidenceFirst_root is not None:
            self.evidenceFirst = evidenceFirst_root.text
        else:
            self.evidenceFirst = None

    def _parse_evidenceLast(self):
        evidenceLast_root = self.root.find(paths["Artist_EvidenceLast_Path"], namespace)
        if evidenceLast_root is not None:
            self.evidenceLast = evidenceLast_root.text
        else:
            self.evidenceLast = None

    def _parse_gender(self):
        gender_root = self.root.find(paths["Artist_Gender_Path"], namespace)
        if gender_root is not None:
            self.gender = gender_root.text
        else:
            self.gender = None

    def _parse_roles(self):
        roles_root = self.root.find(paths["Artist_Roles_Path"], namespace)
        if roles_root is not None:
            self.roles = roles_root.text
        else:
            self.roles = None



    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "alt_labels": self.alt_labels,
            "sourceIDs": self.source_ids,
            "nationality": self.nationality,
            "dateOfBirth": self.birth,
            "dateOfDeath": self.death,
            "evidenceFirst": self.evidenceFirst,
            "evidenceLast": self.evidenceLast,
            "gender": self.gender,
            "roles": self.roles,
            "count": self.count,
            "rank": self.rank,
        }
        return filter_none(json)
