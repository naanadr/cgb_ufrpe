import cv2


def fill_poly(img, points, sides, coords):
    x0, y0 = points[0]
    x1, y1 = points[1]
    x2, y2 = points[2]

    for line in coords:
        for coord in line:
            _plot(img, coord)


def _plot(img, point):
    cv2.circle(img, point, 0, (255, 255, 255), -1)
