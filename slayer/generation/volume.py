
class Volume(object):
    def __init__(self):
        self.__slices = {}
        self.__min = 1
        self.__max = 0

    def add_slice(self, name_data):
        name, data = name_data
        self.__slices[name] = data

        self.__min = min(self.__min, data.min())
        self.__max = max(self.__max, data.max())

    @property
    def slices(self):
        return self.__slices

    @property
    def min(self):
        return self.__min

    @property
    def max(self):
        return self.__max
