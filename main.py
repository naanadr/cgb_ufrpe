from os import getenv, listdir

import cv2
import numpy as np
from dotenv import load_dotenv

from utils import (
    build_malha3d,
    enrich_triangles,
    extract_triangles,
    extract_vertices,
    read_config_file,
    read_file,
)
from utils.preprocess import matrix_change_base
from utils.rasterization import bresenhan_function

RES_X = 512
RES_Y = 512


def main():
    print("## PROJETO 1 V.A. CGB UFRPE 2020.4 ##")

    run()
    load = True
    while load:
        reload = input(
            "\nVocê deseja recarregar a figura com novos parâmetros? (1 - Sim, 0 - Não)  "
        )
        print("\n")
        if reload == "1":
            run()
        elif reload == "0":
            break
        else:
            print("Opção não válida, tente novamente!")


def find_file():
    objects_3d = getenv("OBJECTS_3D")
    file = list(filter(lambda x: ".byu" in x, listdir(objects_3d)))[0]
    print(f"Arquivo utilizado: {file}")

    return objects_3d + file


def run():
    cam_config = read_config_file(getenv("CONFIG_FILE"))
    print(f"Configurações utilizadas: {cam_config}")
    matrix = matrix_change_base(
        V=list(cam_config.get("V")), N=list(cam_config.get("N"))
    )

    lines = read_file(find_file())
    malha3d = build_malha3d(line=lines[0])
    build_triangles(
        malha3d=malha3d,
        lines=lines,
        cam_config=cam_config,
        matrix_change_base=matrix,
    )

    img = np.zeros((RES_X, RES_Y, 3), np.uint8)
    draw_object(img, malha3d)
    show_object(img)


def build_triangles(malha3d, lines, cam_config, matrix_change_base):
    extract_vertices(malha3d=malha3d, lines=lines[1 : malha3d.qtd_vertices + 1])
    extract_triangles(malha3d=malha3d, lines=lines[malha3d.qtd_vertices + 1 :])
    enrich_triangles(
        malha3d=malha3d,
        config=cam_config,
        matrix_change_base=matrix_change_base,
        res_x=RES_X,
        res_y=RES_Y,
    )


def draw_object(img, malha3d):
    for triangle in malha3d.triangles:
        triangle.vector.sort(key=lambda x: x[1])

        points = []
        for i in range(0, len(triangle.vector) - 1):
            points.append((triangle.vector[i], triangle.vector[i + 1]))
        points.append((triangle.vector[0], triangle.vector[-1]))

        for point in points:
            bresenhan_function(img=img, p0=point[0], p1=point[1])


def show_object(img):
    print("\nPressione qualquer tecla para sair!")
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    load_dotenv()

    main()
