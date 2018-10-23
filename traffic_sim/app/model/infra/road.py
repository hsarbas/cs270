import ZODB
import persistent
import const
from math import sqrt
from app.utils import tools


class AbstractRoad(persistent.Persistent):
    """
    Abstract Road class
    """

    def __init__(self, label, src, dst, lanes):
        """
        Initialize abstract road values

        :param label: road label (string)
        :param src: source node (Node object)
        :param dst: destination node (Node object)
        :param lanes: number of lanes

        lane_width: width of a lane (m)
        length: length of the road (m)
        """

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
        """
        Road object representation
        """

        return '<%s>' % self.label


class Link(AbstractRoad):
    """
    Inherits AbstractRoad
    Represents roads in the network
    """

    def __init__(self, label,  src, dst, lanes):
        """
        Initialize link values

        :param label: link label (string)
        :param src: source node (Node object)
        :param dst: destination node (Node object)
        :param lanes: number of lanes
        """

        super(Link, self).__init__(label, src, dst, lanes)


class Connector(AbstractRoad):
    """
    Inherits AbstractRoad
    Represents connections between links (conflicts and intersections)
    """

    def __init__(self, label,  src_road, dst_road, conflict_groups):
        """
        Initialize connector values

        :param label: connector label (string)
        :param src_road: source road (Link object)
        :param dst_road: destination road (Link object)
        :param conflict_groups: conflict group; A connector may belong to many conflict groups; Only two connectors per
        conflict group

        locked: road lock; Agents cannot pass if connector is locked; Handled by ConflictManager
        """

        super(Connector, self).__init__(label, src_road.dst, dst_road.src, src_road.lanes)

        self.src_road = src_road
        self.dst_road = dst_road

        self.conflict_groups = conflict_groups
        self.locked = False
