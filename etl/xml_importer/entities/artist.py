from etl.xml_importer.parseLido import get_id_by_prio
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace


class Artist():

    def __init__(self, root):
        self.root = root
        self.id = self._parse_id()
        self.type = 'artist'
        self.actorId = self._parse_actorID()
        self.name = self._parse_name()
        self.birth = self._parse_birth()
        self.death = self._parse_death()

    def _parse_id(self):
        allArtistIDs = self.root.findall(paths["Artist_ID_Path"], namespace)
        id = get_id_by_prio(allArtistIDs)
        return id

    def _parse_actorID(self):
        allactorIDs = []
        for actorID in self.root.findall(paths["Artist_ID_Path"], namespace):
            allactorIDs.append(SourceID(actorID))
        return allactorIDs

    def _parse_name(self):
        return self.root.find(paths["Artist_Name_Path"], namespace).text

    def _parse_birth(self):
        birthDate = self.root.findall(paths["Artist_Birth_Path"], namespace)
        if len(birthDate) > 0:
            return birthDate[0].text
        else:
            return ''

    def _parse_death(self):
        deathDate = self.root.find(paths["Artist_Death_Path"], namespace)
        if deathDate == None:
            return ''
        else:
            return deathDate.text

    def parse(self):
        pass

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