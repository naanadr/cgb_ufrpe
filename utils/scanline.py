def fill_poly(points, sides, coords):
    # Ordena as coordenadas pelo valor de Y
    side_1 = coords[0]
    side_1.sort(key=lambda x: x[1])
    side_2 = coords[1]
    side_2.sort(key=lambda x: x[1])
    side_3 = coords[2]
    side_3.sort(key=lambda x: x[1])

    inside_points = []
    inside_points.extend(_run_sides(side_1, side_3))

    if side_2[-1] == side_3[0]:
        side_2 = side_2[::-1]

    inside_points.extend(_run_sides(side_2, side_3))

    return inside_points


def _run_sides(side_1, side_2):
    inside_points = []

    for sideA in side_1:
        for sideB in side_2:
            if sideA == sideB:
                continue

            x0, y0 = sideA
            x1, y1 = sideB

            if y1 > y0:
                break
            elif y1 < y0:
                continue

            if x0 > x1:
                x0, x1 = x1, x0

            for x in range(x0, x1 + 1):
                inside_points.append((x, y0))

    return inside_points
