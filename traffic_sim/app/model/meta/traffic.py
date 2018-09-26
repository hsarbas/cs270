from PySide2.QtCore import *


class Dispatcher(QObject):
    def __init__(self, road):
        super(Dispatcher, self).__init__(parent=None)
        self.road = road
        self.clock = None

    def run(self, clock):
        if clock:
            self.clock = clock
            self.clock.fine.connect(self._signal_callback)
        else:
            self.clock = None

    def _signal_callback(self):
        print self.road, 'dispatcher callback'
