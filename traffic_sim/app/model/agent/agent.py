from PySide2.QtCore import *
import movement_model
import const

import itertools
_id_counter = itertools.count()
import random

class Agent(QObject):

    moved = Signal()
    killed = Signal()

    def __init__(self, init_vel, init_acc, route):
        super(Agent, self).__init__(parent=None)
        self.vel = init_vel
        self.acc = init_acc
        self.vel_max = random.choice([3, 5, 10, 15, 20])
        # self.vel_max = const.DESIRED_VELOCITY
        self.acc_max = const.MAXIMUM_ACCELERATION
        self.dec_max = const.MAXIMUM_DECELERATION
        self.length = const.LENGTH
        self.width = const.WIDTH
        self.route = route

        self.position = dict()
        self.neighborhood = dict()
        self.sight_distance = None

        self.id_ = hex(_id_counter.next())

    def deliberate_acc(self):

        front = self.neighborhood['front']
        gap_front = self.neighborhood['gap_front']
        vel_front = front.vel if front else const.LARGE_NUMBER

        acc = movement_model.intelligent_driver_model(self.vel, self.vel_max, self.acc_max, self.dec_max, vel_front, gap_front)
        return acc

    def move(self, vel, acc, road, pos, lane):
        self.vel = vel
        self.acc = acc
        self.position['road'] = road
        self.position['pos'] = pos
        self.position['lane'] = lane

        self.moved.emit()

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id_)

    def __del__(self):
        self.killed.emit()
