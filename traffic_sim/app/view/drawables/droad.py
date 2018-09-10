from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class DLink(QGraphicsLineItem):
    def __init__(self, link):
        super(DLink, self).__init__(parent=None)
        self.object = link

        self.setLine(link.src.x, link.src.y, link.dst.x, link.dst.y)
        self.setPen(QPen(Qt.darkGray, 5.0))


class DConnector(QGraphicsLineItem):
    def __init__(self, connector):
        super(DConnector, self).__init__(parent=None)
        self.object = connector

        self.setLine(connector.src.x, connector.src.y, connector.dst.x, connector.dst.y)
        self.setPen(QPen(Qt.lightGray, 5.0))
