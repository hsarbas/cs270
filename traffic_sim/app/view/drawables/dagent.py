from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from app.utils import tools
import weakref


class DAgent(QGraphicsLineItem):
    def __init__(self, agent):
        super(DAgent, self).__init__(parent=None)

        self._w_agent = weakref.ref(agent)
        self.object.moved.connect(self.responder)

        # self.setLine(10, 10, 50, 10)
        width = tools.to_px(self.object.width)

        pen = QPen()
        pen.setBrush(Qt.black)
        pen.setWidth(width)
        pen.setCapStyle(Qt.RoundCap)
        self.setPen(pen)

        self.setZValue(2)

    @property
    def object(self):
        return self._w_agent()

    def responder(self):
        pos = tools.to_px(self.object.position['pos'])

        self.setLine(pos, 10, pos - tools.to_px(self.object.length), 10)
