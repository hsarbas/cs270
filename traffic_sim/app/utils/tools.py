import const
from math import sqrt


def to_m(px):
    return round(px * const.PX2M_DEFAULT, 2)


def to_px(m):
    return round(int(float(m) / const.PX2M_DEFAULT), 2)


def direction(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0


def delta_pt_in_line(x0, y0, xt, yt, d):
    """
    Computes the vector distance of the point in line from the start point, d distance away.

    :param x0: x-coordinate of the start point
    :param y0: y-coordinate of the start point
    :param xt: x-coordinate of the end point
    :param yt: y-coordinate of the end point
    :param d: distance away of the point from the start point
    :return: vector distance of the point in line from the start point, d distance away.
    """

    dx = xt - x0
    dy = yt - y0

    dir_x = direction(dx)
    dir_y = direction(dy)

    m = dy/float(dx) if dir_x != 0 else 0.0
    mp = dx/float(dy) if dir_y != 0 else 0.0

    delta_x = dir_x * d / sqrt(m ** 2 + 1)
    delta_y = dir_y * d / sqrt(mp ** 2 + 1)

    return delta_x, delta_y


def delta_pt_in_perp_line(x0, y0, xt, yt, d):
    """
    Computes the vector distance of the point perpendicular to the right of the line, d distance away.

    :param x0: x-coordinate of the start point
    :param y0: y-coordinate of the start point
    :param xt: x-coordinate of the end point
    :param yt: y-coordinate of the end point
    :param d: perpendicular distance away of the point from the line
    :return: vector distance of the point perpendicular to the right of the line, d distance away.
    """

    dx = xt - x0
    dy = yt - y0

    dir_x = direction(dx)
    dir_y = direction(dy)

    m = dy/float(dx) if dir_x != 0 else 0.0
    mp = dx/float(dy) if dir_y != 0 else 0.0

    delta_x = -dir_y * d / sqrt(mp ** 2 + 1)
    delta_y = dir_x * d / sqrt(m ** 2 + 1)

    return delta_x, delta_y


def locate_global(road, pos, lane):

    x0, y0 = road.src.x, road.src.y
    xt, yt = road.dst.x, road.dst.y
    # Get global longitude
    long_dx, long_dy = delta_pt_in_line(x0, y0, xt, yt, pos)

    # Get innermost lane
    edge_x, edge_y = delta_pt_in_perp_line(x0, y0, xt, yt, road.width / 2.0)
    ref_x0, ref_y0, ref_xt, ref_yt = x0 - edge_x, y0 - edge_y, xt - edge_x, yt - edge_y

    # Get actual point
    lat_dx, lat_dy = delta_pt_in_perp_line(ref_x0, ref_y0, ref_xt, ref_yt, lane * road.lane_width)

    x = ref_x0 + long_dx + lat_dx
    y = ref_y0 + long_dy + lat_dy

    return round(x, 0), round(y, 0)
