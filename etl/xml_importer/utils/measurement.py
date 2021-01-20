from etl.xml_importer.xpaths import paths, namespace
from etl.xml_importer.parseLido import filter_none


class Measurement:
    def __init__(self, root):
        self.root = root
        self.displayName = ""
        self.type = ""
        self.unit = ""
        self.value = ""
        self.extend = ""
        self.shape = ""
        self.format = ""
        self.qualifier = ""
        self.parse()
        self.clear()

    def parse(self):
        self._parse_displayName()
        self._parse_type()
        self._parse_unit()
        self._parse_value()
        self._parse_extend()
        self._parse_shape()
        self._parse_format()
        self._parse_qualifier()

    def _parse_displayName(self):
        displayName = self.root.find(paths["Measurement_DisplayName_Path"], namespace)
        if displayName is not None:
            self.displayName = displayName.text
        else:
            self.displayName = ""

    def _parse_type(self):
        type = self.root.find(paths["Measurement_Type_Path"], namespace)
        if type is not None:
            self.type = type.text
        else:
            self.type = ""

    def _parse_unit(self):
        unit = self.root.find(paths["Measurement_Unit_Path"], namespace)
        if unit is not None:
            self.unit = unit.text
        else:
            self.unit = ""

    def _parse_value(self):
        value = self.root.find(paths["Measurement_Value_Path"], namespace)
        if value is not None:
            self.value = value.text
        else:
            self.value = ""

    def _parse_extend(self):
        extend = self.root.find(paths["Measurement_Extend_Path"], namespace)
        if extend is not None:
            self.extend = extend.text
        else:
            self.extend = ""

    def _parse_shape(self):
        shape = self.root.find(paths["Measurement_Shape_Path"], namespace)
        if shape is not None:
            self.shape = shape.text
        else:
            self.shape = ""

    def _parse_format(self):
        format = self.root.find(paths["Measurement_Format_Path"], namespace)
        if format is not None:
            self.format = format.text
        else:
            self.format = ""

    def _parse_qualifier(self):
        qualifier = self.root.find(paths["Measurement_Qualifier_Path"], namespace)
        if qualifier is not None:
            self.qualifier = qualifier.text
        else:
            self.qualifier = ""

    def clear(self):
        del self.root

    def __json_repr__(self):
        json = {
            "displayName": self.displayName,
            "type": self.type,
            "unit": self.unit,
            "value": self.value,
            "extend": self.extend,
            "shape": self.shape,
            "format": self.format,
            "qualifier": self.qualifier
        }
        return filter_none(json)
