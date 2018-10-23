from PySide2.QtCore import *
import const


class Clock(QTimer):
    """
    Simulation clock
    Inherits QTimer class

    fine: signal fired by Clock every timestep (DT)
    coarse: signal fired by Clock every 4 timesteps (corresponds to 1 real second)
    """

    fine = Signal()
    coarse = Signal(int)

    def __init__(self):
        """
        Initialize Clock
        """

        super(Clock, self).__init__(parent=None)
        self.dt_fine = const.DT
        self.dt_coarse = const.DT * 4
        self.now = 0

        self.timeout.connect(self.tick)

    def tick(self):
        """
        Responds to 'timeout' signal emitted by QTimer
        """

        self.now += const.DT

        if self.now % self.dt_coarse == 0:
            self.coarse.emit(self.now / self.dt_coarse)
        self.fine.emit()

    def run(self):
        """
        Start clock
        Fires 'timeout' signal every <self.dt_fine> milliseconds
        """

        self.start(self.dt_fine)

    def pause(self):
        """
        Pause clock
        """

        self.stop()

    def reset(self):
        """
        Reset clock
        """

        self.stop()
        self.now = 0
