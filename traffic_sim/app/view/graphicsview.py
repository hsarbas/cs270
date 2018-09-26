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
        self.scene.clear()

        for link_label in ['link 1', 'link 2', 'link 3']:
            link = self.scene.db['roads']['links'][link_label]
            self.scene.add_link(link)

            if link_label in self.scene.db['dispatchers']:
                dispatcher = self.scene.db['dispatchers'][link_label]
                self.scene.add_dispatcher(dispatcher)

            dlink = factory.create_dlink(link)
            self.addItem(dlink)

            dnode_src = factory.create_dnode(link.src)
            dnode_dst = factory.create_dnode(link.dst)
            self.addItem(dnode_src)
            self.addItem(dnode_dst)

        for conn_label in ['conn 1', 'conn 2']:
            conn = self.scene.db['roads']['connectors'][conn_label]
            self.scene.add_connector(conn)

            dconn = factory.create_dconnector(conn)
            self.addItem(dconn)
