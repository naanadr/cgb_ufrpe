from utils import draw


def fill_poly(img, points, sides, coords):
    # Ordena as coordenadas pelo valor de Y
    side_1 = coords[0]
    side_1.sort(key=lambda x: x[1])
    side_2 = coords[1]
    side_2.sort(key=lambda x: x[1])
    side_3 = coords[2]
    side_3.sort(key=lambda x: x[1])

    # Pinta os pixels da borda
    for side in coords:
        for coord in side:
            draw(img, coord)

    _run_sides(img, side_1, side_3)

    if side_2[-1] == side_3[0]:
        side_2 = side_2[::-1]

    _run_sides(img, side_2, side_3)


def _run_sides(img, side_1, side_2):
    for sideA in side_1:
        for sideB in side_2:
            x0, y0 = sideA
            x1, y1 = sideB

            if y1 > y0:
                break
            elif y1 < y0:
                continue

            if x0 > x1:
                x0, x1 = x1, x0

            for x in range(x0, x1 + 1):
                draw(img, (x, y0))
