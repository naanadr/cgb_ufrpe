import numpy as np
import math


class MatrizOperations(object):

    def __init__(self, value_a=None, value_b=None):
        self.value_a = value_a
        self.value_b = value_b

    def _shape(self, value):
        m, n = np.shape(value)
        return m, n

    def _mult_verify(self):
        matriza_linha, matriza_coluna = self._shape(self.value_a)
        matrizb_linha, matrizb_coluna = self._shape(self.value_b)

        if matriza_coluna != matrizb_linha:
            raise ValueError('Tamanho de matrizes incompativel!')

    def multiplication(self):
        """
            Realiza multiplicação de matrizes
        """
        self._mult_verify()

        matriza_linha, matriza_coluna = self._shape(self.value_a)
        matrizb_linha, matrizb_coluna = self._shape(self.value_b)

        new_matriz = []

        for linha_a in range(matriza_linha):
            linha = []
            for coluna_b in range(matrizb_coluna):
                value = 0
                for linha_b in range(matrizb_linha):
                    val_a = self.value_a[linha_a][linha_b]
                    val_b = self.value_b[linha_b][coluna_b]

                    value += val_a * val_b

                linha.append(value)

            new_matriz.append(linha)

        return new_matriz


class SpaceOperations(object):

    def __init__(self, vetor_a=None, vetor_b=None):
        self.vetor_a = vetor_a
        self.vetor_b = vetor_b

    def produto_escalar(self):
        if len(self.vetor_a) != len(self.vetor_b):
            raise "Vetores de tamanhos diferentes!"

        new_vetor = []

        for i in range(len(self.vetor_a)):
            new_vetor.append(self.vetor_a[i]*self.vetor_b[i])

        return sum(new_vetor)

    def produto_vetorial(self):
        if len(self.vetor_a) != len(self.vetor_b):
            raise "Vetores de tamanhos diferentes!"

        i = ((self.vetor_a[1] * self.vetor_b[2]) -
             (self.vetor_a[2] * self.vetor_b[1]))
        j = ((self.vetor_a[2] * self.vetor_b[0]) -
             (self.vetor_a[0] * self.vetor_b[2]))
        k = ((self.vetor_a[0] * self.vetor_b[1]) -
             (self.vetor_a[1] * self.vetor_b[0]))

        return [i, j, k]

    def normal(self, vetor):
        power = [i**2 for i in vetor]
        return math.sqrt(sum(power))
