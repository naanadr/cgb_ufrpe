"""
    Implementação baseada no pseudocódigo descrito no artigo
    https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
    que engloba todos os casos.
"""


def find_points(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    points = []

    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            points = plotLineLow(points, x1, y1, x0, y0)
        else:
            points = plotLineLow(points, x0, y0, x1, y1)
    else:
        if y0 > y1:
            points = plotLineHigh(points, x1, y1, x0, y0)
        else:
            points = plotLineHigh(points, x0, y0, x1, y1)

    return points


def plotLineHigh(points, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1

    if dx < 0:
        xi = -1
        dx = -dx

    D = (2 * dx) - dy
    x = x0

    for y in range(y0, y1 + 1):
        points.append((x, y))
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2 * dx

    return points


def plotLineLow(points, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1

    if dy < 0:
        yi = -1
        dy = -dy

    D = (2 * dy) - dx
    y = y0

    for x in range(x0, x1 + 1):
        points.append((x, y))
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2 * dy

    return points
