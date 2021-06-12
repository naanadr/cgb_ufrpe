from os import getenv, listdir

import cv2
import numpy as np
from dotenv import load_dotenv

from utils import (
    build_malha3d,
    enrich_triangles,
    read_config_file,
    read_file,
)
from utils.math_ops import base_ortonormal
from utils.bresenhan import find_points
from utils.scanline import fill_poly

RES_X = 512
RES_Y = 512


def main():
    print("## PROJETO 1 V.A. CGB UFRPE ##")

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


def run():
    # Carrega os padrões de câmera
    cam_config = read_config_file(getenv("CONFIG_FILE"))
    print(f"Configurações utilizadas: {cam_config}")
    base = base_ortonormal(V=list(cam_config.get("V")), N=list(cam_config.get("N")))

    # Constroi a Malha3D com os valores dos vertices e triangulos
    lines = read_file(file_name=find_file())
    malha3d = build_malha3d(lines=lines)

    # Faz todas as operações necessárias para que o triangulo esteja pronto
    # para ser pintado e mostrado na tela
    enrich_triangles(
        malha3d=malha3d,
        config=cam_config,
        base_ortonormal=base,
        res_x=RES_X,
        res_y=RES_Y,
    )

    img = np.zeros((RES_X, RES_Y, 3), np.uint8)
    draw_object(img, malha3d)
    show_object(img)


def find_file():
    dir_files_objects_3d = getenv("DIR_FILES_OBJECTS_3D")
    file = list(filter(lambda x: ".byu" in x, listdir(dir_files_objects_3d)))[0]
    print(f"Arquivo utilizado: {file}")

    return dir_files_objects_3d + file


def draw_object(img, malha3d):
    for triangle in malha3d.triangles:
        coords = []
        triangle.vector.sort(key=lambda x: x[1])

        points = []
        for i in range(0, len(triangle.vector) - 1):
            points.append((triangle.vector[i], triangle.vector[i + 1]))
        points.append((triangle.vector[0], triangle.vector[-1]))

        for point in points:
            coords.append(find_points(p0=point[0], p1=point[1]))

        fill_poly(img=img, points=triangle.vector, sides=points, coords=coords)


def show_object(img):
    print("\nPressione qualquer tecla para sair!")
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    load_dotenv()

    main()
