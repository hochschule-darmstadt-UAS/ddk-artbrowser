#TODO: noch ueberarbeiten

class Measurment():
    def __init__(self, displayName,
                 #measurementType, unit, value,
                 #extend, shape, format,
                 #qualifier,
                 #measurments_sets
                 ):
        #self.root = measurments_sets
        self.displayName = displayName
        #self.parse()

    def parse(self):
       # self.measurment["displaySize"] = self.root[0].findall(paths["Artwork_Mesurments_DisplaySize_Path"], namespace)[0].text
       # self.measurment["type"] = self.root[0].findall(paths["Artwork_Mesurments_Type_Path"], namespace)[0].text
       # self.measurment["unit"] = self.root[0].findall(paths["Artwork_Mesurments_Unit_Path"], namespace)[0].text
       # self.measurment["value"] = self.root[0].findall(paths["Artwork_Mesurments_Value_Path"], namespace)[0].text

        measurmentsets = []
        for measurments_set in self.root:
        #    measurmentset = measurments_set.findall('lido:displayObjectMeasurements', namespace)
          #  if len(measurmentset) > 0:
         #       measurmentsets.append(measurmentset[0].text)
         #   else:
      #          pass

          #  shape = measurments_set.findall(paths["Artwork_Mesurments_Shape_Path"], namespace)
         #   if len(shape) > 0:
          #      self.measurment["shape"] = shape[0].text
          #  else:
          #      pass

          #  format = measurments_set.findall(paths["Artwork_Mesurments_Format_Path"], namespace)
            if len(format) > 0:
                self.measurment["format"] = format[0].text
            else:
                pass

          #  qualifier = measurments_set.findall(paths["Artwork_Mesurments_Qualifier_Path"], namespace)
          #  if len(qualifier) > 0:
          #      self.measurment["qualifier"] = qualifier[0].text
           # else:
           #     pass

        self.measurment["displaySize"] = measurmentsets[0]

        if len(measurmentsets) > 1:
            self.measurment["displayName"] = measurmentsets[1]
        else:
            pass

    def getmeasurment(self):
        return self.measurment


#displayName string
#measurementType string 2
#unit string 2
#value string 2
#extend string 2
#shape string 2
#format string 2
#qualifier string 2