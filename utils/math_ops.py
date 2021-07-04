from math import floor, sqrt

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
    V = _normalizar(V)
    N = _normalizar(N)
    U = _build_u_value(N, V)

    return [U, V, N]


def coord_vista(P, config, base_ortonormal):
    """
    Essa função converte um ponto em coordenada mundial para coordenada de vista:

    .. math::
        P'= \left [ I \right ]_{\alpha }^{\varepsilon } * (P - C)
    """
    return np.dot(base_ortonormal, np.subtract(P, config.get("C")))


def coordenadas_tela(coordenadas_vista, config, res_x, res_y):
    coordenadas_normalizadas = [
        (config.get("d") * coordenadas_vista[0]) / (res_x * coordenadas_vista[2]),
        (config.get("d") * coordenadas_vista[1]) / (res_y * coordenadas_vista[2]),
    ]

    const_i = ((coordenadas_normalizadas[0] + 1) / 2) * res_x
    const_j = ((coordenadas_normalizadas[1] + 1) / 2) * res_y

    return [
        floor(const_i + 0.5),
        floor(res_y - const_j + 0.5),
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


def find_normal_ponto(coord_baricentrica, norm_vertices):
    multi = [
        np.dot(coord_baricentrica[i], vert) for i, vert in enumerate(norm_vertices)
    ]
    return _normalizar(np.sum(multi, axis=0))


def find_baricentro_triangulo(vertices, config, base_ortonormal):
    vertice_a, vertice_b, vertice_c = vertices
    return [sum(group) / 3 for group in zip(vertice_a, vertice_b, vertice_c)]


def find_baricentro_ponto(ponto, vertice_a, vertice_b, vertice_c):
    """
    A partir de um ponto P (em coordenada de tela) obtido pelo scan line, e
    dos vertices que compõe a superfice onde está esse ponto P, é realizada a
    conversão do R2 para o R3 desse ponto utilizando as coordenadas baricentricas.
    """
    a = vertice_a[0] - vertice_c[0]
    b = vertice_b[0] - vertice_c[0]
    c = vertice_a[1] - vertice_c[1]
    d = vertice_b[1] - vertice_c[1]

    matrix = np.array([[ponto[0] - vertice_c[0]], [ponto[1] - vertice_c[1]]])
    T = [
        [a, b],
        [c, d],
    ]
    det = np.linalg.det(T)
    if det == 0.0:
        return False

    T_inv = np.linalg.inv(T)
    alfa, beta = np.matmul(T_inv, matrix)
    gama = 1 - alfa - beta

    return (alfa[0], beta[0], gama[0])


def find_p_original(coordenada_barizentrica, coordenadas_vista):
    alfa, beta, gama = coordenada_barizentrica
    vertice_a, vertice_b, vertice_c = coordenadas_vista

    return [
        np.sum([alfa * vertice_a[0], beta * vertice_b[0], gama * vertice_c[0]]),
        np.sum([alfa * vertice_a[1], beta * vertice_b[1], gama * vertice_c[1]]),
        np.sum([alfa * vertice_a[2], beta * vertice_b[2], gama * vertice_c[2]]),
    ]
