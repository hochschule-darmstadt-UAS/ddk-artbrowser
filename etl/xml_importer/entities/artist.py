from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Artist():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()

    def _parse_id(self):
        allArtistIDs = self.root.findall(paths["Artist_ID_Path"], namespace)
        id = get_id_by_prio(allArtistIDs)
        return id

    def parse(self):
        self.entity_type = 'Artist'
        self.concepts = []
        self.label = self.root.find(paths["Artist_Name_Path"], namespace).text

        for source_id in self.root.findall(paths["Artist_ID_Path"], namespace):
            concept = SourceID(source_id)
            self.concepts.append(concept)

        self.birth = self._parse_birth()
        self.death = self._parse_death()

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
        return {
            "id": self.id,
            "entityType": self.entity_type,
            "label": self.label,
            "sourceID": self.concepts,
            "dateOfBirth": self.birth,
            "dateOfDeath": self.death,
        }

#id
#entityType string
#actorID SourceID[]
#name string
#altNames string 2
#nationality string 2
#birth string
#death string
#evidenceFirst string 2
#evidenceLast string 2
#gender string 2
#roles string 2