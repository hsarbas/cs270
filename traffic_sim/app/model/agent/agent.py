from PySide2.QtCore import *
import movement_model
import const

import itertools
_id_counter = itertools.count()


class Agent(QObject):
    """
    moved: signal fired by agent after updating its values (received by DAgent)
    killed: signal fired by agent after exiting road network (received by DAgent)

    intention_enter: signal fired by agent before entering an intersection (received by ConflictManager)
    intention_exit: signal fired by agent before exiting an intersection (received by ConflictManager)
    """

    moved = Signal()
    killed = Signal()

    intention_enter = Signal(dict)
    intention_exit = Signal(dict)

    def __init__(self, init_vel, init_acc, route):
        """
        Initialize agent

        :param init_vel: initial velocity (m/s)
        :param init_acc: initial acceleration (m/s^2)
        :param route: route (list of road labels to be traversed by agent)
        """

        super(Agent, self).__init__(parent=None)
        self.vel = init_vel
        self.acc = init_acc
        self.vel_max = const.DESIRED_VELOCITY
        self.acc_max = const.MAXIMUM_ACCELERATION
        self.dec_max = const.MAXIMUM_DECELERATION
        self.length = const.LENGTH
        self.width = const.WIDTH
        self.route = route

        self.position = dict()
        self.neighborhood = dict()  # 'front' -> Agent object, 'gap_front' -> meters
        self.sight_distance = None
        self.next_conflict = None
        self.time_active = 0.0

        self.id_ = hex(_id_counter.next())

    def deliberate_acc(self):
        """
        Determine agent acceleration

        acc_idm: acceleration due to car-following
        acc_conflict: acceleration due to intersection

        :return: minimum of acc_idm and acc_conflict
        """

        acc_list = []

        front = self.neighborhood['front']
        gap_front = self.neighborhood['gap_front']
        vel_front = front.vel if front else const.LARGE_NUMBER

        acc_idm = movement_model.intelligent_driver_model(self.vel, self.vel_max, self.acc_max, self.dec_max,
                                                              vel_front, gap_front)
        acc_list.append(acc_idm)

        acc_conflict = self.react_to_conflict()
        acc_list.append(acc_conflict)

        return min(acc_list)

    def react_to_conflict(self):
        """
        Handles agent reaction to conflicts and intersections

        :return: acceleration due to intersection
        """
        acc = const.LARGE_NUMBER

        if self.next_conflict:
            self.intention_enter.emit(dict(road=self.next_conflict, gap=self.neighborhood['gap_front']))

            if self.next_conflict.locked:
                dist_from_conflict = self.position['road'].length - self.position['pos']
                acc = movement_model.intelligent_driver_model(self.vel, self.vel_max, self.acc_max, self.dec_max,
                                                              0.0,
                                                              dist_from_conflict)

        # else:
        #     if 'road' in self.position and self.position['road'].__class__.__name__ == 'Connector':
        #         if self.position['road'].length - self.position['pos'] <= 2.0:
        #             self.intention_exit.emit(dict(road=self.position['road']))

        return acc

    def move(self, vel, acc, road, pos, lane, next_conflict):
        """
        Update agent values

        :param vel: new velocity (m/s)
        :param acc: new acceleration (m/s^2)
        :param road: new road (road object)
        :param pos: new position relative to start of road (m)
        :param lane: new lane
        :param next_conflict: conflict/intersection in nearest to agent
        """

        self.vel = vel
        self.acc = acc
        self.position['road'] = road
        self.position['pos'] = pos
        self.position['lane'] = lane
        self.next_conflict = next_conflict

        self.moved.emit()

    def __repr__(self):
        """
        Agent representation when print method is called
        """
        return '<%s: %s>' % (self.__class__.__name__, self.id_)

    def __del__(self):
        """
        Delete agent object
        """

        self.killed.emit()
