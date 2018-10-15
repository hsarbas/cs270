from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from app.model.scene import Scene
from app.controller import factory


class GraphicsView(QGraphicsView):
    def __init__(self, parent, db):
        super(GraphicsView, self).__init__(parent=parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)

        self.canvas = GraphicsScene(parent, db)
        self.canvas.setSceneRect(0, 0, 10000, 10000)
        self.setScene(self.canvas)
        self.centerOn(0, 0)


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent, db):
        super(GraphicsScene, self).__init__(parent=parent)
        self.scene = Scene(db)

    def add_merging_conflict(self):
        self.scene.clear()
        self.clear()

        for link_label in ['link 1', 'link 2', 'link 3']:
            link = self.scene.db['roads']['links'][link_label]
            self.scene.add_link(link)

            dlink = factory.create_dlink(link)
            self.addItem(dlink)

        for conn_label in ['conn 1', 'conn 2']:
            conn = self.scene.db['roads']['connectors'][conn_label]
            self.scene.add_connector(conn)

            dconn = factory.create_dconnector(conn)
            self.addItem(dconn)

    def add_diverging_conflict(self):
        self.scene.clear()
        self.clear()

    def add_crossing_conflict(self):
        self.scene.clear()
        self.clear()

    def add_dagent(self, agent):
        if agent:
            dagent = factory.create_dagent(self, agent)
            self.addItem(dagent)

    def remove_dagent(self, dagent):
        self.removeItem(dagent)
        del dagent

    def recolor(self, run=True):
        if run:
            for item in self.items():
                if item.__class__.__name__ == 'DLink':
                    pen = item.pen()
                    pen.setBrush(Qt.lightGray)
                    item.setPen(pen)
        else:
            for item in self.items():
                if item.__class__.__name__ == 'DLink':
                    pen = item.pen()
                    pen.setBrush(Qt.darkGray)
                    item.setPen(pen)
