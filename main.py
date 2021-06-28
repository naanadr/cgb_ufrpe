from os import getenv, listdir

import cv2
import numpy as np
from dotenv import load_dotenv

from objects.z_buffer import Malha_ZBuffer
from utils import (
    build_malha3d,
    draw,
    enrich_triangles,
    enrich_vertices,
    find_pixels,
    read_config_file,
    read_file,
)
from utils.math_ops import base_ortonormal, find_p_original

RES_X = 512
RES_Y = 512


def main():
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
    zbuffer_malha = Malha_ZBuffer(RES_X, RES_Y)
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
    # Adiciona as normais aos vertices que compõe essa malha 3d
    enrich_vertices(malha3d=malha3d)

    malha3d.sort_triangles()

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
        pixels = find_pixels(triangle)
        pixels_original = []
        # Valor dos pixels no R3
        for pixel in pixels:
            pixels_original.append(
                find_p_original(
                    pixel, triangle.vertices_coord_tela, triangle.vertices_coord_vista
                )
            )
            draw(img, pixel)

        # Valor do ponto no R2 e no R3
        triangle.inside_points = zip(pixels, pixels_original)


def show_object(img):
    print("\nPressione qualquer tecla para sair!")
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    load_dotenv()

    main()
