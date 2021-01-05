class Triangle:
    def __init__(self, index_x, index_y, index_z):
        self.index_x = index_x
        self.index_y = index_y
        self.index_z = index_z
        self.vector = None

    @property
    def index_x(self):
        return self.__index_x

    @index_x.setter
    def index_x(self, value):
        self.__index_x = int(value)

    @property
    def index_y(self):
        return self.__index_y

    @index_y.setter
    def index_y(self, value):
        self.__index_y = int(value)

    @property
    def index_z(self):
        return self.__index_z

    @index_z.setter
    def index_z(self, value):
        self.__index_z = int(value)
