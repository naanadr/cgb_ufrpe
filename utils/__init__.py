from os import getenv

import cv2
from dotenv import load_dotenv

from utils.malha3d import Malha3D
from utils.triangle import Triangle
from utils.vertex import Vertex
from utils.preprocess import convert_coord


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

    return cam_config


def build_malha3d(line):
    values = line.split(" ")

    malha3d = Malha3D(qtd_vertices=values[0], qtd_triangles=values[1])

    return malha3d


def extract_vertices(malha3d, lines):
    for line in lines:
        values = line.split(" ")

        vertex = Vertex(x=values[0], y=values[1], z=values[2])
        malha3d.add_vertex(vertex)


def extract_triangles(malha3d, lines):
    for line in lines:
        values = line.split(" ")

        triangle = Triangle(index_x=values[0], index_y=values[1], index_z=values[2])
        malha3d.add_triangle(triangle)


def enrich_triangles(malha3d, **kwargs):
    for triangle in malha3d.triangles:
        triangle.vector = [
            convert_coord(P=malha3d.vertices[triangle.index_x].get(), **kwargs),
            convert_coord(P=malha3d.vertices[triangle.index_y].get(), **kwargs),
            convert_coord(P=malha3d.vertices[triangle.index_z].get(), **kwargs),
        ]


def draw(img, point):
    cv2.circle(img, point, 0, (255, 255, 255), -1)
