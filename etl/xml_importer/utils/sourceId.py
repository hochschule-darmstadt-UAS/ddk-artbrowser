from etl.xml_importer.xpaths import namespace, paths


class SourceID:

    def __init__(self, root, term_path='lido:term'):
        self.root = root
        self.term_path = term_path

        self.source = ""

        self.id = self._parse_id()
        if self.id is not None:
            self.source = self._parse_source()
        self.terms = self._parse_terms()

    def _parse_id(self):
        return self.root.text

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
            terms.append(term_root.text)

        return terms

    def __json_repr__(self):
        return {
            "id": self.id,
            "source": self.source,
            "terms": self.terms
        }