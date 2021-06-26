from math import sqrt

import numpy as np


def _ortogonalizar(V, N):
    """Essa função ortonaliza o valor de V:

    .. math::
        V'= V - \frac{\left \langle V, N \right \rangle}{\left \langle N, N \right \rangle} * N
    """

    return np.subtract(V, np.dot((np.dot(V, N) / np.dot(N, N)), N))


def _build_u_value(N, V):
    return np.cross(N, V)


def _normalizar(vector):
    """Essa função normaliza um determinado vetor:

    .. math::
        v = (x, y, z)
        \left \|v  \right \| = \sqrt{\left \langle v, v \right \rangle}
        \left \|v  \right \| = \sqrt{x^{2} + y^{2} + z^{2}}
        \bar{v} = \frac{v}{\left \|v  \right \|}
    """
    return np.divide(vector, sqrt(np.dot(vector, vector)))


def base_ortonormal(V, N):
    """
    Constroi a base ortonormal no sistema de vista.
    1 - Ortogonaliza V
    2 - Normaliza V e N
    3 - Calcula U
    4 - Retorna a base ortonormal [U, V, N]
    """
    V = _ortogonalizar(V, N)
    U = _build_u_value(N, V)

    norm_V = _normalizar(V)
    norm_N = _normalizar(N)
    norm_U = _normalizar(U)

    return [norm_U, norm_V, norm_N]


def _coord_vista(P, config, base_ortonormal):
    """
    Essa função converte um ponto em coordenada mundial para coordenada de vista:

    .. math::
        P'= \left [ I \right ]_{\alpha }^{\varepsilon } * (P - C)
    """
    return np.dot(base_ortonormal, np.subtract(P, config.get("C")))


def _coordenadas_tela(coord_vista, config, res_x, res_y):
    coordenadas_normalizadas = [
        config.get("d/hx") * (coord_vista[0] / coord_vista[2]),
        config.get("d/hy") * (coord_vista[1] / coord_vista[2]),
    ]

    return [
        int(((coordenadas_normalizadas[0] + 1) / 2) * (res_x + 0.5)),
        int(res_y - ((coordenadas_normalizadas[1] + 1) / 2) * res_y + 0.5),
    ]


def convert_coord(P, config, base_ortonormal, res_x, res_y):
    """
    A partir de uma coordenada mundial, é realizada a conversão para coordenada
    de vista e depois para coordenada de tela.
    """
    coord_vista = _coord_vista(P, config, base_ortonormal)
    coord_tela = _coordenadas_tela(coord_vista, config, res_x, res_y)

    return coord_tela


def find_normal(value1, value2, value3, config, base_ortonormal):
    """
    Calcula a normal de uma superfice a partir de três valores e normaliza esse
    resultado.

    1 - Se for um triangulo, utilizar as três vertices;
    1.1 - Calcular o produto vetorial de v2 - v1 e v3 - v1
    1.2 - Utilizar a regra da mão esquerda, para fazer o produto vetorial
    1.3 - Normalizar o vetor resultante
    """
    value1 = _coord_vista(value1, config, base_ortonormal)
    value2 = _coord_vista(value2, config, base_ortonormal)
    value3 = _coord_vista(value3, config, base_ortonormal)

    v1 = np.subtract(value2, value1)
    v2 = np.subtract(value3, value1)
    prod_vetorial = np.cross(v1, v2)

    return _normalizar(prod_vetorial)
