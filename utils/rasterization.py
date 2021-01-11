"""
    Implementação baseada em https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
"""
import cv2


def bresenhan_function(img, p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    plotLine(img, x0, y0, x1, y1)

    return img


def plotLine(img, x0, y0, x1, y1):
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            plotLineLow(img, x1, y1, x0, y0)
        else:
            plotLineLow(img, x0, y0, x1, y1)
    else:
        if y0 > y1:
            plotLineHigh(img, x1, y1, x0, y0)
        else:
            plotLineHigh(img, x0, y0, x1, y1)


def _plot(img, point):
    cv2.circle(img, point, 0, (255, 255, 255), -1)


def plotLineHigh(img, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1

    if dx < 0:
        xi = -1
        dx = -dx

    D = (2 * dx) - dy
    x = x0

    for y in range(y0, y1 + 1):
        _plot(img, (x, y))
        if D > 0:
            x = x + xi
            D = D + (2 * (dx - dy))
        else:
            D = D + 2 * dx


def plotLineLow(img, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1

    if dy < 0:
        yi = -1
        dy = -dy

    D = (2 * dy) - dx
    y = y0

    for x in range(x0, x1 + 1):
        _plot(img, (x, y))
        if D > 0:
            y = y + yi
            D = D + (2 * (dy - dx))
        else:
            D = D + 2 * dy


# def bresenhan_function(img, p1, p2):
#     exception = False
#     # if p1[0] > p2[0]:
#     #     p1, p2 = p2, p1
#
#     x0, y0 = p1
#     x1, y1 = p2
#
#     deltax = x1 - x0
#     deltay = y1 - y0
#
#     error = 0
#     try:
#         deltaerr = abs(float(deltay / deltax))
#     except ZeroDivisionError:
#         exception = True
#
#     y = y0
#     if exception:
#         x = x0
#         for y in range(y0, y1 + 1):
#             cv2.circle(img, (x, y), 0, (255, 255, 255), -1)
#     else:
#         if x0 > x1:
#             range_x = range(160, 154 - 1, -1)
#             import ipdb
#
#             ipdb.set_trace()
#         else:
#             range_x = range(x0, x1 + 1)
#
#         for x in range_x:
#             cv2.circle(img, (x, y), 0, (255, 255, 255), -1)
#
#             error += deltaerr
#             if error >= 0.5:
#                 error -= 1.0
#             if deltay != 0:
#                 y += 1
#
#     return img
