import ZODB
import persistent


class Node(persistent.Persistent):
    def __init__(self, x, y, dir_):
        super(Node, self).__init__()

        self.x = x
        self.y = y
        self.dir_ = dir_
