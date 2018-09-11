from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from app.utils import tools


class DLink(QGraphicsLineItem):
    def __init__(self, link):
        super(DLink, self).__init__(parent=None)
        self.object = link

        self.setLine(link.src.x, link.src.y, link.dst.x, link.dst.y)
        width = tools.to_px(link.lanes * link.lane_width)

        pen = QPen()
        pen.setBrush(Qt.darkGray)
        pen.setWidth(width)
        pen.setCapStyle(Qt.FlatCap)
        self.setPen(pen)

        self.setZValue(1)


class DConnector(QGraphicsLineItem):
    def __init__(self, connector):
        super(DConnector, self).__init__(parent=None)
        self.object = connector

        self.setLine(connector.src.x, connector.src.y, connector.dst.x, connector.dst.y)
        width = tools.to_px(connector.lanes * connector.lane_width)

        pen = QPen()
        pen.setBrush(Qt.lightGray)
        pen.setWidth(width)
        pen.setCapStyle(Qt.FlatCap)
        self.setPen(pen)

        self.setZValue(0)
