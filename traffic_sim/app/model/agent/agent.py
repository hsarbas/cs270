import ZODB
import persistent
import const

import itertools
_id_counter = itertools.count()


class Agent(persistent.Persistent):

    def __init__(self, init_vel, init_acc):
        self.vel = init_vel
        self.acc = init_acc
        self.vel_max = const.DESIRED_VELOCITY
        self.acc_max = const.MAXIMUM_ACCELERATION
        self.dec_max = const.MAXIMUM_DECELERATION
        self.length = const.LENGTH
        self.width = const.WIDTH

        self.id_ = hex(_id_counter.next())

    def deliberate_acc(self):
        return 1.0

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.id_)
