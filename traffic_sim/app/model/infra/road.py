import ZODB
import persistent
import const
from math import sqrt


class AbstractRoad(persistent.Persistent):
    def __init__(self, src, dst, lanes):
        super(AbstractRoad, self).__init__()

        self.src = src
        self.dst = dst
        self.lanes = lanes
        self.lane_width = const.LANE_WIDTH

        self.dx = self.dst.x - self.src.x
        self.dy = self.dst.y - self.src.y
        self.length = sqrt(self.dx ** 2 + self.dy ** 2)


class Link(AbstractRoad):
    def __init__(self, src, dst, lanes):
        super(Link, self).__init__(src, dst, lanes)


class Connector(AbstractRoad):
    def __init__(self, src_road, dst_road):
        super(Connector, self).__init__(src_road.dst, dst_road.src, src_road.lanes)
