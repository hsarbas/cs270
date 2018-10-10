from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from app.utils import tools
import weakref


class DAgent(QGraphicsLineItem):
    def __init__(self, agent, road, pos, lane):
        super(DAgent, self).__init__(parent=None)

        self._w_agent = weakref.ref(agent)

    @property
    def object(self):
        return self._w_agent()
