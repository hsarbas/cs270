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
        self.canvas.setSceneRect(0, 0, 800, 400)
        self.setScene(self.canvas)
        self.centerOn(0, 0)


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent, db):
        super(GraphicsScene, self).__init__(parent=parent)
        self.scene = Scene(db)

    def add_merging_conflict(self):
        for link in self.scene.db['roads']['links']:
            dlink = factory.create_dlink(link)
            self.addItem(dlink)
