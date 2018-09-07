import ZODB
import persistent
from app.utils import exceptions


class Node(persistent.Persistent):
    def __init__(self, x, y, dir_):
        super(Node, self).__init__()

        self.x = x
        self.y = y

        if dir_ not in ['src', 'dst']:
            raise exceptions.InvalidNodeDirectionError

        self.dir_ = dir_
