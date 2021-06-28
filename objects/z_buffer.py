class Malha_ZBuffer:
    def __init__(self, res_x, res_y):
        self.res_x = res_x
        self.res_y = res_y
        self.matriz = []

        self._init_matriz()

    def _init_matriz(self):
        for i in range(self.res_x):
            i = []
            for j in range(self.res_y):
                i.append(ZBuffer())
            self.matriz.append(i)


class ZBuffer:
    def __init__(self):
        self.cor = (0, 0, 0)
        self.profundidade = float("+inf")
        self.ponto = None
