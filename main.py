from os import getenv, listdir

from dotenv import load_dotenv

from utils import build_malha3d, extract_triangles, extract_vertices, read_file


def main():
    objects_3d = getenv("OBJECTS_3D")

    files_info = []
    files = listdir(objects_3d)

    for file in files:
        file_name = objects_3d + file
        lines = read_file(file_name)

        malha3d = build_malha3d(file_name=file_name, line=lines[0])

        extract_vertices(malha3d=malha3d, lines=lines[1 : malha3d.qtd_vertices + 1])
        extract_triangles(malha3d=malha3d, lines=lines[malha3d.qtd_vertices + 1 :])

        files_dict = {"shape": file, "malha3d": malha3d}
        files_info.append(files_dict)


if __name__ == "__main__":
    load_dotenv()

    main()
