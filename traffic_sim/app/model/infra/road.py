import ZODB
import persistent
import const
from math import sqrt
from app.utils import tools


class AbstractRoad(persistent.Persistent):
    def __init__(self, label, src, dst, lanes):
        super(AbstractRoad, self).__init__()

        self.label = label
        self.src = src
        self.dst = dst
        self.lanes = lanes
        self.lane_width = const.LANE_WIDTH
        self.width = self.lanes * self.lane_width

        self.dx = self.dst.x - self.src.x
        self.dy = self.dst.y - self.src.y
        self.length = tools.to_m(sqrt(self.dx ** 2 + self.dy ** 2))

    def __repr__(self):
        return '<%s>' % self.label


class Link(AbstractRoad):
    def __init__(self, label,  src, dst, lanes):
        super(Link, self).__init__(label, src, dst, lanes)


class Connector(AbstractRoad):
    def __init__(self, label,  src_road, dst_road, conflict_groups):
        super(Connector, self).__init__(label, src_road.dst, dst_road.src, src_road.lanes)

        self.src_road = src_road
        self.dst_road = dst_road

        self.conflict_groups = conflict_groups
        self.locked = False
