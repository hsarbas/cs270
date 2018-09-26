from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import weakref


class Dispatcher(QObject):
    def __init__(self, road):
        super(Dispatcher, self).__init__(parent=None)
        self._road = weakref.ref(road)

    @property
    def road(self):
        return self._road()
