from etl.xml_importer.xpaths import namespace
from etl.xml_importer.parseLido import sanitize_id, sanitize, filter_none

import  logging


class SourceID:

    def __init__(self, root, term_path='lido:term'):
        self.root = root
        self.term_path = term_path

        self.source = ""

        self.id = self._parse_id()
        if self.id is not None:
            self.source = self._parse_source()
        self.terms = self._parse_terms()
        logging.info('A sourceID was parsed from xml file complete.')
        logging.info('Clear sourceID.')
        self.clear()

    def _parse_id(self):
        id = sanitize_id(self.root.text)
        return id

    def _parse_source(self):
        attributes = self.root.attrib
        if attributes.get('lido:source', namespace):
            source_attribute_key = '{' + namespace['lido'] + '}source'
            source = self.root.attrib.get(source_attribute_key)
            return source
        else:
            return None

    def _parse_terms(self):
        terms = []
        term_roots = self.root.getparent().findall(self.term_path, namespace)
        for term_root in term_roots:
            term = sanitize(term_root.text)
            terms.append(term)

        return terms

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "id": self.id,
            "source": self.source,
            "terms": self.terms
        }
        return filter_none(json)
