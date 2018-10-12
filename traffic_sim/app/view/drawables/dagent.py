from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from app.utils import tools
import weakref


class DAgent(QGraphicsLineItem):
    def __init__(self, gc, agent):
        super(DAgent, self).__init__(parent=None)

        self.gc = gc
        self._w_agent = weakref.ref(agent)
        self.object.moved.connect(self.responder)
        self.object.killed.connect(self.delete_)

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

        road = self.object.position['road']
        pos = tools.to_px(self.object.position['pos'])
        lane = self.object.position['lane']

        front_x, front_y = tools.locate_global(road, pos, lane + 0.5)
        rear_x, rear_y = tools.locate_global(road, pos - tools.to_px(self.object.length), lane + 0.5)
        self.setLine(rear_x, rear_y, front_x, front_y)

    def delete_(self):
        self.gc.remove_dagent(self)
