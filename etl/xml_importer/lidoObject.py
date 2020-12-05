import xml.etree.ElementTree as xml
import json
import copy
from xpaths import paths
import utils

namespace = {'lido': 'http://www.lido-schema.org'}

class LidoObject():
    def __init__(self, root):
        self.root = root
       # self.artwork = None
      #  self.parse()

    #def parse(self):
      #  self.artwork = Artwork(self.root)._get_Artwork()

