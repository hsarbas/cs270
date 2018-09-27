from PySide2.QtCore import *
import random


class Dispatcher(QObject):

    dispatch_agent = Signal()

    def __init__(self, road):
        super(Dispatcher, self).__init__(parent=None)
        self.road = road
        self.clock = None

        self.flow_rate = None

    def run(self, clock):
        self.flow_rate = random.choice([1, 2, 3, 4, 5])

        if clock:
            self.clock = clock
            self.clock.coarse.connect(self._signal_callback)
        else:
            self.clock = None

    def _signal_callback(self, time):
        if time % self.flow_rate == 0:
            self.dispatch_agent.emit()
