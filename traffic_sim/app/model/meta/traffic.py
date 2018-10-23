from PySide2.QtCore import *
import random


class Dispatcher(QObject):
    """
    Dispatcher class

    dispatch_agent: signal fired by dispatcher when current time is a multiple of dispatcher flow rate
    (received by simulation engine)
    """

    dispatch_agent = Signal(dict)

    def __init__(self, road):
        """
        Initialize Dispatcher

        :param road: road to which the dispatcher is attached; Road object
        flow_rate: dispatch agent every x seconds
        """

        super(Dispatcher, self).__init__(parent=None)
        self.road = road
        self.clock = None

        self.flow_rate = None

    def run(self, clock):
        """
        Activate dispatcher at the start of simulation

        :param clock: Clock object
        :return:
        """

        self.flow_rate = 10
        # self.flow_rate = random.choice([3, 5, 7, 9])

        if clock:
            self.clock = clock
            self.clock.coarse.connect(self._signal_callback)
        else:
            self.clock = None

    def _signal_callback(self, time):
        """
        Responds to 'coarse' signal emitted by Clock

        :param time: current time
        """

        if time % self.flow_rate == 0:
            lanes = []
            for lane in range(self.road.lanes):
                lanes.append(lane)

            init_val = dict(init_vel=0.0,
                            init_acc=0.0,
                            road=self.road,
                            pos=0.0,
                            lane=random.choice(lanes))

            self.dispatch_agent.emit(init_val)
