from os import getenv, listdir

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

RES_X = 100
RES_Y = 100


def main():
    cam_config = read_config_file(getenv("CONFIG_FILE"))
    matrix = matrix_change_base(
        V=list(cam_config.get("V")), N=list(cam_config.get("N"))
    )

    objects_3d = getenv("OBJECTS_3D")

    # TODO: Receber do usuário o nome do arquivo que será lido
    files = listdir(objects_3d)
    file = files[0]
    file_name = objects_3d + file

    lines = read_file(file_name)

    malha3d = build_malha3d(file_name=file_name, line=lines[0])

    extract_vertices(malha3d=malha3d, lines=lines[1 : malha3d.qtd_vertices + 1])
    extract_triangles(malha3d=malha3d, lines=lines[malha3d.qtd_vertices + 1 :])
    enrich_triangles(
        malha3d=malha3d,
        config=cam_config,
        matrix_change_base=matrix,
        res_x=RES_X,
        res_y=RES_Y,
    )


if __name__ == "__main__":
    load_dotenv()

    main()
