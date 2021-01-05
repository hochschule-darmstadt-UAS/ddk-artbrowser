from etl.xml_importer.utils.rights import Rights
from etl.xml_importer.utils.sourceId import SourceID
from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.parseLido import sanitize, filter_none


class Resource:
    def __init__(self, root):
        self.root = root
        self.resourceIDs = self._parse_resourceID()
        self.resourceType = self._parse_resourceType()
        self.rights = self._parse_rights()
        self.resourceDateTaken = self._parse_resourceDateTaken()
        self.linkResource = self._parse_linkResource()
        self.photographer = self._parse_photographer()
        self.clear()

    def _parse_resourceID(self):
        id_root = self.root.find(paths["Resource_resourceID_Path"], namespace)
        if id_root is not None:
            return SourceID(id_root)
        else:
            return None

    def _parse_resourceType(self):
        resource_type_root = self.root.find(paths["Resource_resourceType_Path"], namespace)
        return sanitize(resource_type_root.text)

    def _parse_rights(self):#Todo
        right_root = self.root.find(paths["Resource_Rights_Path"], namespace)
        rights = Rights(right_root)
        return rights


    def _parse_resourceDateTaken(self):
        resource_dateTaken_root = self.root.find(paths["Resource_ResourceDateTaken_Path"], namespace)
        if resource_dateTaken_root is not None:
            return resource_dateTaken_root.text

    def _parse_linkResource(self):
        link_resource_root = self.root.find(paths["Resource_LinkResource_Path"], namespace)
        if link_resource_root is not None:
            return link_resource_root.text
        else:
            return ""

    def _parse_photographer(self):
        resource_photographer_root = self.root.find(paths["Resource_Photographer_Path"], namespace)
        if resource_photographer_root is not None:
            return resource_photographer_root.text

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "resourceIDs": self.resourceIDs,
            "rights": self.rights,
            "dateTaken": self.resourceDateTaken,
            "photographer": self.photographer,
            "resourceType": self.resourceType,
            "linkResource": self.linkResource,
        }
        return filter_none(json)
