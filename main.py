from os import getenv, listdir

from dotenv import load_dotenv

from utils import (
    build_malha3d,
    extract_triangles,
    extract_vertices,
    read_file,
    read_config_file,
)


def main():
    objects_3d = getenv("OBJECTS_3D")
    cam_config = read_config_file(getenv("CONFIG_FILE"))

    # TODO: Receber do usuário o nome do arquivo que será lido
    files = listdir(objects_3d)
    file = files[0]
    file_name = objects_3d + file

    lines = read_file(file_name)

    malha3d = build_malha3d(file_name=file_name, line=lines[0])

    extract_vertices(malha3d=malha3d, lines=lines[1 : malha3d.qtd_vertices + 1])
    extract_triangles(malha3d=malha3d, lines=lines[malha3d.qtd_vertices + 1 :])


if __name__ == "__main__":
    load_dotenv()

    main()
