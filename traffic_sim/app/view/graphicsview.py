from PySide2.QtGui import *
from PySide2.QtWidgets import *
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
        for link in self.scene.db['roads']['links'].values():
            dlink = factory.create_dlink(link)
            self.addItem(dlink)

            dnode_src = factory.create_dnode(link.src)
            dnode_dst = factory.create_dnode(link.dst)
            self.addItem(dnode_src)
            self.addItem(dnode_dst)

        for conn in self.scene.db['roads']['connectors'].values():
            dconn = factory.create_dconnector(conn)
            self.addItem(dconn)
