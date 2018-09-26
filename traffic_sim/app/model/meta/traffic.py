from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import weakref


class Dispatcher(QObject):
    def __init__(self, road):
        super(Dispatcher, self).__init__(parent=None)
        self._road = weakref.ref(road)
        self._agent_manager = None

    @property
    def road(self):
        return self._road()

    def run(self, agent_manager):
        if agent_manager:
            self._agent_manager = weakref.ref(agent_manager)
        else:
            self._agent_manager = None

    def _signal_callback(self):
        pass
