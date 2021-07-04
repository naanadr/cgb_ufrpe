class Malha3D:
    def __init__(self, qtd_vertices, qtd_triangles):
        self.qtd_vertices = qtd_vertices
        self.qtd_triangles = qtd_triangles
        self.vertices = []
        self.triangles = []

    @property
    def qtd_vertices(self):
        return self.__qtd_vertices

    @qtd_vertices.setter
    def qtd_vertices(self, value):
        self.__qtd_vertices = int(value)

    @property
    def qtd_triangles(self):
        return self.__qtd_triangles

    @qtd_triangles.setter
    def qtd_triangles(self, value):
        self.__qtd_triangles = int(value)

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    def sort_triangles(self):
        aux = [(t, t.baricentro) for t in self.triangles]
        aux.sort(key=lambda x: x[1][2])
        self.triangles = [t[0] for t in aux]
