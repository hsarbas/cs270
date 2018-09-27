from PySide2.QtCore import *
import const


class Clock(QTimer):

    fine = Signal()
    coarse = Signal(int)

    def __init__(self):
        super(Clock, self).__init__(parent=None)
        self.dt_fine = const.DT
        self.dt_course = const.DT * 4
        self.now = 0

        self.timeout.connect(self.tick)

    def tick(self):
        self.now += const.DT

        if self.now % self.dt_course == 0:
            self.coarse.emit(self.now / self.dt_course)
        self.fine.emit()

    def run(self):
        self.start(self.dt_fine)

    def pause(self):
        self.stop()

    def reset(self):
        self.stop()
        self.now = 0
