from PySide2.QtCore import *
import random
from app.model.agent import const


class Dispatcher(QObject):
    """
    Dispatcher class

    dispatch_agent: signal fired by dispatcher when current time is a multiple of dispatcher flow rate
    (received by simulation engine)
    """

    dispatch_agent = Signal(dict)

    def __init__(self, road, agent_manager):
        """
        Initialize Dispatcher

        :param road: road to which the dispatcher is attached; Road object
        :param agent_manager: AgentManager object
        flow_rate: dispatch agent every x seconds
        """

        super(Dispatcher, self).__init__(parent=None)
        self.road = road
        self.clock = None
        self.agent_manager = agent_manager

        self.flow_rate = None

    def run(self, clock):
        """
        Activate dispatcher at the start of simulation

        :param clock: Clock object
        :return:
        """

        self.flow_rate = 5
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
            lane = random.choice(lanes)

            if self.spatial_clearance(lane):
                init_val = dict(init_vel=0.0,
                                init_acc=0.0,
                                road=self.road,
                                pos=0.0,
                                lane=lane)

                self.dispatch_agent.emit(init_val)

    def spatial_clearance(self, lane):
        """
        Determine if there is enough clearance for a given lane to dispatch new agent

        :param lane:
        :return: True if enough clearance; otherwise False
        """

        if self.agent_manager.members(self.road, start=0.0, end=const.DISPATCH_REACH, lane=lane):
            return False

        return True
