from abc import abstractmethod, ABCMeta
import json

# This interface should be implemented by all entity and utility classes
class JSONEncodable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __json_repr__(self): raise NotImplementedError


# This class is used as json encoder for classes that implement the JSONEncodable interface
# Usage: json.dumps(artwork, cls=ComplexJSONEncoder)
class ComplexJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json_repr__'):
            return obj.__json_repr__()
        else:
            return json.JSONEncoder.default(self, obj)
