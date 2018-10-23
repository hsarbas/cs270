from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from app.utils import tools
import weakref


class DLink(QGraphicsLineItem):
    """
    Link drawable class
    Inherits QGraphicsLineItem
    """

    def __init__(self, link):
        """
        Initialize DLink

        :param link: Link object
        """
        super(DLink, self).__init__(parent=None)
        self._w_link = weakref.ref(link)

        self.setLine(self.object.src.x, self.object.src.y, self.object.dst.x, self.object.dst.y)
        width = tools.to_px(self.object.lanes * self.object.lane_width)

        pen = QPen()
        pen.setBrush(Qt.darkGray)
        pen.setWidth(width)
        pen.setCapStyle(Qt.FlatCap)
        self.setPen(pen)

        self.setZValue(1)

    @property
    def object(self):
        """
        :return: Link object referenced (weakly) by self._w_link
        """
        return self._w_link()


class DConnector(QGraphicsLineItem):
    """
    Connector drawable class
    Inherits QGraphicsLineItem
    """

    def __init__(self, connector):
        """
        Initialize DConnector

        :param connector: Connector object
        """
        super(DConnector, self).__init__(parent=None)
        self._w_conn = weakref.ref(connector)

        self.setLine(self.object.src.x, self.object.src.y, self.object.dst.x, self.object.dst.y)
        width = tools.to_px(self.object.lanes * self.object.lane_width)

        pen = QPen()
        pen.setBrush(Qt.lightGray)
        pen.setWidth(width)
        pen.setCapStyle(Qt.FlatCap)
        self.setPen(pen)

        self.setZValue(0)

    @property
    def object(self):
        """
        :return: Connector object referenced (weakly) by self._w_conn
        """

        return self._w_conn()
