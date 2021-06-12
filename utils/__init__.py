from os import getenv

import cv2
from dotenv import load_dotenv

from objects.malha3d import Malha3D
from objects.triangle import Triangle
from objects.vertex import Vertex
from utils.math_ops import convert_coord, find_normal


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
        point_x = malha3d.vertices[triangle.index_x].get()
        point_y = malha3d.vertices[triangle.index_y].get()
        point_z = malha3d.vertices[triangle.index_z].get()

        triangle.vector = [
            convert_coord(P=point_x, **kwargs),
            convert_coord(P=point_y, **kwargs),
            convert_coord(P=point_z, **kwargs),
        ]


def draw(img, point):
    cv2.circle(img, point, 0, (255, 255, 255), -1)
