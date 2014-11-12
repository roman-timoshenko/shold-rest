import logging
import math

logger = logging.getLogger(__name__)
DEFAULT_EPSILON = 0.001


def get_distance(a, b):
    """
    Calculates distance between two given points.

    get_instance((0, 0), (0, 1)) will result in 1.0.

    :type a: (float, float)
    :param a: a tuple of floats representing a point, first number in tuple stands fot 'x' coordinate, second - 'y'
    :type b: (float, float)
    :param b: a tuple of floats representing a point, first number in tuple stands fot 'x' coordinate, second - 'y'
    :rtype: float
    :return: distance between two given points
    """
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def intersect(x0, y0, r0, x1, y1, r1):
    """
    Checks if two circles do intersect.

    :type x0: float
    :param x0: first circle center X coordinate
    :type y0: float
    :param y0: first circle center Y coordinate
    :type r0: float
    :param r0: first circle center radius
    :type x1: float
    :param x1: second circle center X coordinate
    :type y1: float
    :param y1: second circle center Y coordinate
    :type r1: float
    :param r1: second circle center radius
    :rtype: bool
    :return: true if two circles do intersect, false otherwise
    """
    d = get_distance((x0, y0), (x1, y1))
    if d > r0 + r1:
        return False
    if d < math.fabs(r0 - r1):
        return False
    return True


def find_circle_intersections(x0, y0, r0, x1, y1, r1):
    """
    Finds two points of intersection for two circles.

    :type x0: float
    :param x0: first circle center X coordinate
    :type y0: float
    :param y0: first circle center Y coordinate
    :type r0: float
    :param r0: first circle radius
    :type x1: float
    :param x1: second circle center X coordinate
    :type y1: float
    :param y1: second circle center Y coordinate
    :type r1: float
    :param r1: second circle radius
    :rtype: ((float, float), (float, float))
    :return: two coordinates of circles intersection
    :raise ValueError: when circles do not intersect
    """
    d = get_distance((x0, y0), (x1, y1))
    if d > r0 + r1:
        raise ValueError('circles are not intersecting: too far from each other')
    if d < math.fabs(r0 - r1):
        raise ValueError('circles are not intersecting: one inside another')

    a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(math.fabs(r0 ** 2 - a ** 2))

    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d

    xa3 = x2 + h * (y1 - y0) / d
    ya3 = y2 - h * (x1 - x0) / d

    xb3 = x2 - h * (y1 - y0) / d
    yb3 = y2 + h * (x1 - x0) / d

    return (xa3, ya3), (xb3, yb3)


def get_fourth_point(a, b, c, ad, bd, cd, epsilon=DEFAULT_EPSILON):
    """
    Finds fourth point assuming three distances to three known points.

    :type a: (float, float)
    :param a: tuple, point one, e.g. (0, 0)
    :type b: (float, float)
    :param b: tuple, point two, e.g. (0, 1)
    :type c: (float, float)
    :param c: tuple, point three, e.g. (1, 1)
    :type ad: float
    :param ad: distance from point a to unknown point d
    :type bd: float
    :param bd: distance from point b to unknown point d
    :type cd: float
    :param cd: distance from point c to unknown point d
    :type epsilon: float
    :param epsilon: calculation precision, defaults to DEFAULT_EPSILON value
    :rtype: (float, float)
    :return: tuple representing a point of that distances from another three points
    :raise ValueError: when fourth point cannot be found
    """
    try:
        first, second = find_circle_intersections(a[0], a[1], ad, b[0], b[1], bd)
    except ValueError as e:
        logger.info(e)
        raise ValueError('intersection point cannot be found, please, verify data', e)

    distance_to_first = get_distance(c, first)
    distance_to_second = get_distance(c, second)

    if math.fabs(distance_to_first - distance_to_second) < epsilon:
        raise ValueError('cannot find intersection point correctly, please, verify data')

    if math.fabs(round(distance_to_first) - cd) < (epsilon + 1):
        return first
    if math.fabs(round(distance_to_second) - cd) < (epsilon + 1):
        return second
    # if math.fabs(distance_to_second - cd) > epsilon:
    # first_second=(distance_to_first, distance_to_second)
    #        first.y=
    #        return first_second
    raise ValueError('intersection point cannot be found, please, verify data')


def is_point_in_circle(cx, cy, cr, x, y):
    """
    Calculates if a point is inside circle.

    :type cx: float
    :param cx: circle x-coordinate
    :type cy: float
    :param cy: circle y-coordinate
    :type cr: float
    :param cr: circle radius
    :type x: float
    :param x: point x-coordinate
    :type y: float
    :param y: point y-coordinate
    :rtype: bool
    :return: true if point is in circle, false otherwise
    """
    distance_from_center = get_distance((cx, cy), (x, y))
    return distance_from_center < cr