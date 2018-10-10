from PySide2.QtCore import *

import const

import itertools
_id_counter = itertools.count()


class Agent(QObject):

    moved = Signal()

    def __init__(self, init_vel, init_acc):
        super(Agent, self).__init__(parent=None)
        self.vel = init_vel
        self.acc = init_acc
        self.vel_max = const.DESIRED_VELOCITY
        self.acc_max = const.MAXIMUM_ACCELERATION
        self.dec_max = const.MAXIMUM_DECELERATION
        self.length = const.LENGTH
        self.width = const.WIDTH

        self.position = dict()

        self.id_ = hex(_id_counter.next())

    def deliberate_acc(self):
        return 1.0

    def move(self, vel, acc, road, pos, lane):
        self.vel = vel
        self.acc = acc
        self.position['road'] = road
        self.position['pos'] = pos
        self.position['lane'] = lane

        self.moved.emit()

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id_)
