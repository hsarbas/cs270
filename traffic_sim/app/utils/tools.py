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


def compute_ssd(velocity, grav=const.G, friction=const.F, perc_time=const.PRT, min_ssd=const.MIN_SIGHT_DIST):
    """
    Stopping sight distance (SSD) is a near worst-case distance a vehicle driver needs to be able to see in order
    have room to stop before colliding with an object ahead of the road.

    SSD is composed of the following:
    (1) Perception-Reaction Distance
         - the distance it takes for a road user to realize that a reaction is needed due to a road condition
         - equal to agent's velocity (in m/s) times the perception-reaction time (2.5 seconds)
    (2) Braking Distance
        - the distance it takes to complete the maneuver (braking)
        - equal to agent's velocity  (in m/s) divided by the product of twice the weight force acceleration
            due to gravity (19.6 m/s^2) and coefficient of friction between car tires and asphalt roads

    :param velocity: Velocity of sensing agent in m/s
    :param grav: Gravitational acceleration in m/s^2
    :param friction: Friction coefficient between car tires and road
    :param perc_time: Perception time in sec
    :param min_ssd: Minimum SSD in meters

    :return: SSD of the sensing agent in METERS. Minimum of 15.0 meters
    """
    braking_dist = velocity ** 2 / (grav * 2.0 * friction)
    perception_reaction_dist = velocity * perc_time
    ssd = braking_dist + perception_reaction_dist

    ssd = max(min_ssd, ssd)  # in m

    return ssd
