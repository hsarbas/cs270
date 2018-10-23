import ZODB
import persistent
from app.utils import exceptions


class Node(persistent.Persistent):
    """
    Road source/destination
    """

    def __init__(self, x, y, dir_):
        """
        Initialize node values

        :param x: x-coordinate
        :param y: y-coordinate
        :param dir_: direction ('src' - source, 'dst' - destination)
        """
        super(Node, self).__init__()

        self.x = x
        self.y = y

        if dir_ not in ['src', 'dst']:
            raise exceptions.InvalidNodeDirectionError

        self.dir_ = dir_
