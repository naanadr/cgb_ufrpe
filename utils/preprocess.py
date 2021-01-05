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


def matrix_change_base(V, N):
    V = _ortogonalizar(V, N)
    U = _build_u_value(N, V)

    norm_V = _normalizar(V)
    norm_N = _normalizar(N)
    norm_U = _normalizar(U)

    return [norm_U, norm_V, norm_N]


def convert_coord(P, config, matrix_change_base, res_x, res_y):
    """Essa função converte um ponto em coordenada mundial para coordenada de vista:

    .. math::
        P'= \left [ I \right ]_{\alpha }^{\varepsilon } * (P - C)
    """
    cood_vista = np.dot(matrix_change_base, np.subtract(P, config.get("C")))
    cood_tela = [
        (config.get("d") / config.get("hx")) * (cood_vista[0] / cood_vista[1]),
        (config.get("d") / config.get("hy")) * (cood_vista[1] / cood_vista[2]),
    ]

    return [
        int(((cood_tela[0] + 1) / 2) * (res_x + 0.5)),
        int(res_y - ((cood_tela[1] + 1) / 2) * res_y + 0.5),
    ]
