import copy
from os import getenv

import cv2
from dotenv import load_dotenv

from objects.malha3d import Malha3D
from objects.triangle import Triangle
from objects.vertex import Vertex
from utils.bresenhan import find_points
from utils.math_ops import (
    coord_vista,
    coordenadas_tela,
    find_baricentro_triangulo,
    find_normal_triangle,
    find_normal_vertice,
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
    }

    cam_config["d/hx"] = cam_config.get("d") / cam_config.get("hx")
    cam_config["d/hy"] = cam_config.get("d") / cam_config.get("hy")

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
    for triangle in malha3d.triangles:
        vertice_x = malha3d.vertices[triangle.index_x]
        vertice_x.triangles.append(triangle)
        vertice_y = malha3d.vertices[triangle.index_y]
        vertice_y.triangles.append(triangle)
        vertice_z = malha3d.vertices[triangle.index_z]
        vertice_z.triangles.append(triangle)

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
        triangle.normal = find_normal_triangle(triangle.vertices_coord_vista)
        triangle.baricentro = find_baricentro_triangulo(
            triangle.vertices_coord_vista, kwargs["config"], kwargs["base_ortonormal"]
        )


def enrich_vertices(malha3d):
    for vertice in malha3d.vertices:
        vertice.normal = find_normal_vertice(vertice)


def find_pixels(triangle):
    vertices = copy.deepcopy(triangle.vertices_coord_tela)
    vertices.sort(key=lambda x: x[1])
    # Lista com pares de coordenadas
    # Cada par representa o começo e o fim de um lateral do triangulo
    # No total são 3 pares de coordenadas
    coords_sides = []
    for i in range(0, len(triangle.vertices_coord_tela) - 1):
        coords_sides.append((vertices[i], vertices[i + 1]))
    coords_sides.append((vertices[0], vertices[-1]))

    # Encontra os pontos que foram as retas (lados) do triangulo
    coords_inside_sides = []
    for point in coords_sides:
        coords_inside_sides.append(find_points(p0=point[0], p1=point[1]))

    return fill_poly(
        points=triangle.vertices_coord_tela,
        sides=coords_sides,
        coords=coords_inside_sides,
    )


def draw(img, point):
    cv2.circle(img, point, 0, (255, 255, 255), -1)
