from abc import abstractmethod, ABCMeta

class JSONEncodable:
    __metaclass__= ABCMeta

    @abstractmethod
    def __json_repr__(self): raise NotImplementedError