from PySide2.QtCore import *
import random


class Dispatcher(QObject):

    dispatch_agent = Signal(dict)

    def __init__(self, road):
        super(Dispatcher, self).__init__(parent=None)
        self.road = road
        self.clock = None

        self.flow_rate = None

    def run(self, clock):
        self.flow_rate = random.choice([3, 6])
        # self.flow_rate = random.choice([6, 9, 12])
        # self.flow_rate = 10

        if clock:
            self.clock = clock
            self.clock.coarse.connect(self._signal_callback)
        else:
            self.clock = None

    def _signal_callback(self, time):
        if time % self.flow_rate == 0:
            init_val = dict(init_vel=0.0,
                            init_acc=0.0,
                            road=self.road,
                            pos=0.0,
                            lane=0)

            self.dispatch_agent.emit(init_val)
