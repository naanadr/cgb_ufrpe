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


def coord_vista(P, config, base_ortonormal):
    """
    Essa função converte um ponto em coordenada mundial para coordenada de vista:

    .. math::
        P'= \left [ I \right ]_{\alpha }^{\varepsilon } * (P - C)
    """
    return np.dot(base_ortonormal, np.subtract(P, config.get("C")))


def coordenadas_tela(coordenadas_vista, config, res_x, res_y):
    coordenadas_normalizadas = [
        config.get("d/hx") * (coordenadas_vista[0] / coordenadas_vista[2]),
        config.get("d/hy") * (coordenadas_vista[1] / coordenadas_vista[2]),
    ]

    return [
        int(((coordenadas_normalizadas[0] + 1) / 2) * (res_x + 0.5)),
        int(res_y - ((coordenadas_normalizadas[1] + 1) / 2) * res_y + 0.5),
    ]


def find_normal_triangle(coordenadas_vista):
    """
    Calcula a normal de uma superfice a partir de três valores e normaliza esse
    resultado.

    Para um determinado triangulo, utilizar as três vertices;
    1 - Calcular o produto vetorial de v2 - v1 e v3 - v1
    2 - Utilizar a regra da mão esquerda, para fazer o produto vetorial
    3 - Normalizar o vetor resultante
    """
    value1, value2, value3 = coordenadas_vista

    v1 = np.subtract(value2, value1)
    v2 = np.subtract(value3, value1)
    prod_vetorial = np.cross(v1, v2)

    return _normalizar(prod_vetorial)


def find_normal_vertice(vertice):
    """
    Para um determinado vertice, é encontrado a normal dele de acordo com as
    normais dos triangulos que utilizam esse vertice.
    """
    norm_triangles = [t.normal for t in vertice.triangles]
    return _normalizar(np.sum(norm_triangles, axis=0))


def find_baricentro_triangulo(vertices, config, base_ortonormal):
    vertice_x, vertice_y, vertice_z = vertices

    return [sum(group) / 3 for group in zip(vertice_x, vertice_y, vertice_z)]


def _find_baricentro_ponto(ponto, vertice_x, vertice_y, vertice_z):
    """
    A partir de um ponto P (em coordenada de tela) obtido pelo scan line, e
    dos vertices que compõe a superfice onde está esse ponto P, é realizada a
    conversão do R2 para o R3 desse ponto utilizando as coordenadas baricentricas.
    """
    a = vertice_x[0] - vertice_z[0]
    b = vertice_y[0] - vertice_z[0]
    c = vertice_x[1] - vertice_z[1]
    d = vertice_y[1] - vertice_z[1]

    try:
        T = np.array(
            [
                [a, b],
                [c, d],
            ]
        )
        T_inv = np.linalg.inv(T)
        matrix = np.array([[ponto[0] - vertice_z[0]], [ponto[1] - vertice_z[1]]])
        alfa, beta = np.matmul(T_inv, matrix)
        gama = 1 - alfa - beta

        return (alfa[0], beta[0], gama[0])
    except Exception as e:
        import ipdb

        ipdb.set_trace()
        return (0, 0, 0)


def find_p_original(ponto, coordenadas_tela, coordenadas_vista):
    alfa, beta, gama = _find_baricentro_ponto(
        ponto,
        coordenadas_tela[0],
        coordenadas_tela[1],
        coordenadas_tela[2],
    )

    return np.sum(
        [
            np.dot(alfa, coordenadas_vista[0]),
            np.dot(beta, coordenadas_vista[1]),
            np.dot(gama, coordenadas_vista[2]),
        ],
        axis=0,
    )
