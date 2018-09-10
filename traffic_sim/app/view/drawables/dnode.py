from PySide2.QtWidgets import *
from PySide2.QtCore import *


class DNode(QGraphicsEllipseItem):
    def __init__(self, node):
        super(DNode, self).__init__(parent=None)
        self.object = node
        self.setRect(node.x, node.y, 5.0)

        if node.dir_ == 'src':
            self.setBrush(Qt.green)
        elif node.dir_ == 'dst':
            self.setBrush(Qt.red)
