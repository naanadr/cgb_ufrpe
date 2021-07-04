import copy
from os import getenv

import cv2
import numpy as np
from dotenv import load_dotenv

from objects.malha3d import Malha3D
from objects.point import Point
from objects.triangle import Triangle
from objects.vertex import Vertex
from utils.bresenhan import find_points
from utils.math_ops import (
    coord_vista,
    coordenadas_tela,
    find_baricentro_ponto,
    find_baricentro_triangulo,
    find_normal_triangle,
    find_normal_vertice,
    find_p_original,
)
from utils.scanline import fill_poly


def read_file(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        lines = list(map(lambda line: line.replace("\n", ""), lines))

        return lines


def read_config_file(file_name):
    load_dotenv(file_name, override=True)
    cam_config = {
        "N": eval(getenv("N")),
        "V": eval(getenv("V")),
        "d": eval(getenv("d")),
        "hx": eval(getenv("hx")),
        "hy": eval(getenv("hy")),
        "C": eval(getenv("C")),
        "Ka": eval(getenv("Ka")),
        "Iamb": eval(getenv("Iamb")),
        "Kd": eval(getenv("Kd")),
        "Od": eval(getenv("Od")),
        "Il": eval(getenv("Il")),
        "Ks": eval(getenv("Ks")),
        "n": eval(getenv("n")),
        "Pl": eval(getenv("Pl")),
    }

    return cam_config


def _extract_vertices(malha3d, lines):
    for line in lines:
        values = line.split(" ")

        vertex = Vertex(x=values[0], y=values[1], z=values[2])
        malha3d.add_vertex(vertex)


def _extract_triangles(malha3d, lines):
    for line in lines:
        values = line.split(" ")

        triangle = Triangle(index_x=values[0], index_y=values[1], index_z=values[2])
        malha3d.add_triangle(triangle)


def _filter_triangle(triangle):
    vertice_a, vertice_b, vertice_c = triangle.vertices_coord_tela
    if vertice_a == vertice_b or vertice_a == vertice_c or vertice_b == vertice_c:
        return False
    else:
        matriz = [
            [vertice_a[0], vertice_a[1], 1],
            [vertice_b[0], vertice_b[1], 1],
            [vertice_c[0], vertice_c[1], 1],
        ]
        det = np.linalg.det(matriz)
        if det == 0.0:
            return False
        else:
            return True


def build_malha3d(lines):
    """
    Constroi Malha3D com a quantidade de vertices e triangulos presentes
    no arquivo .byu

    Além disso, adiciona nessa Malha todos os objetos dos tipos vertices e
    triangulos que estão presentes nele.
    """
    line = lines[0]
    values = line.split(" ")

    malha3d = Malha3D(qtd_vertices=values[0], qtd_triangles=values[1])
    _extract_vertices(malha3d=malha3d, lines=lines[1 : malha3d.qtd_vertices + 1])
    _extract_triangles(malha3d=malha3d, lines=lines[malha3d.qtd_vertices + 1 :])

    return malha3d


def enrich_triangles(malha3d, **kwargs):
    """
    Carrega as vertices presentes na Malha3D e insere os seu valores
    convertidos de coordenadas mundiais para coordenadas de vista.

    Além disso, encontra a normal de cada triangulo e insere o valor
    no atributo `normal`
    """
    good_triangles = []
    for triangle in malha3d.triangles:
        vertice_x = malha3d.vertices[triangle.index_x]
        vertice_y = malha3d.vertices[triangle.index_y]
        vertice_z = malha3d.vertices[triangle.index_z]

        triangle.vertices_coord_vista = [
            coord_vista(
                vertice_x.get(),
                kwargs["config"],
                kwargs["base_ortonormal"],
            ),
            coord_vista(
                vertice_y.get(),
                kwargs["config"],
                kwargs["base_ortonormal"],
            ),
            coord_vista(
                vertice_z.get(),
                kwargs["config"],
                kwargs["base_ortonormal"],
            ),
        ]
        triangle.vertices_coord_tela = [
            coordenadas_tela(
                triangle.vertices_coord_vista[0],
                kwargs["config"],
                kwargs["res_x"],
                kwargs["res_y"],
            ),
            coordenadas_tela(
                triangle.vertices_coord_vista[1],
                kwargs["config"],
                kwargs["res_x"],
                kwargs["res_y"],
            ),
            coordenadas_tela(
                triangle.vertices_coord_vista[2],
                kwargs["config"],
                kwargs["res_x"],
                kwargs["res_y"],
            ),
        ]

        if _filter_triangle(triangle) is True:
            vertice_x.triangles.append(triangle)
            vertice_y.triangles.append(triangle)
            vertice_z.triangles.append(triangle)

            triangle.normal = find_normal_triangle(triangle.vertices_coord_vista)
            triangle.baricentro = find_baricentro_triangulo(
                triangle.vertices_coord_vista,
                kwargs["config"],
                kwargs["base_ortonormal"],
            )
            good_triangles.append(triangle)

    malha3d.triangles = good_triangles


def enrich_vertices(malha3d):
    for vertice in malha3d.vertices:
        vertice.normal = find_normal_vertice(vertice)


def _find_pixels(vertices_coord_tela, sort_vertices_coord_tela):

    # Lista com pares de coordenadas
    # Cada par representa o começo e o fim de um lateral do triangulo
    # No total são 3 pares de coordenadas
    coords_sides = []
    for i in range(0, len(vertices_coord_tela) - 1):
        coords_sides.append(
            (sort_vertices_coord_tela[i], sort_vertices_coord_tela[i + 1])
        )
    coords_sides.append((sort_vertices_coord_tela[0], sort_vertices_coord_tela[-1]))

    # Encontra os pontos que foram as retas (lados) do triangulo
    coords_inside_sides = []
    for point in coords_sides:
        coords_inside_sides.append(find_points(p0=point[0], p1=point[1]))

    return fill_poly(
        points=vertices_coord_tela,
        sides=coords_sides,
        coords=coords_inside_sides,
    )


def _update_zbuffer_malha(malha, point):
    x, y = point.pixel
    element_in_malha = malha.matriz[x][y]
    if element_in_malha.profundidade > point.p_original[2]:
        element_in_malha.profundidade = point.p_original[2]
        element_in_malha.ponto = point


def enrich_points(malha3d, zbuffer_malha):
    for triangle in malha3d.triangles:
        vertices_coord_tela = triangle.vertices_coord_tela
        sort_vertices_coord_tela = copy.deepcopy(vertices_coord_tela)
        sort_vertices_coord_tela.sort(key=lambda x: x[1])

        all_pixels = _find_pixels(vertices_coord_tela, sort_vertices_coord_tela)

        filter_pixels = []
        for pixel in all_pixels:
            result = find_baricentro_ponto(pixel, *sort_vertices_coord_tela)
            if result is False:
                continue
            else:
                p_original = find_p_original(result, triangle.vertices_coord_vista)
                point = Point(
                    pixel=pixel, coord_baricentrica=result, coord_original=p_original
                )
                filter_pixels.append(point)
                _update_zbuffer_malha(zbuffer_malha, point)

        triangle.inside_points = filter_pixels


def draw(img, point):
    cv2.circle(img, point, 0, (255, 255, 255), -1)
