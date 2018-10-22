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
        self.parent = parent
        self.setMouseTracking(True)

        self.canvas = GraphicsScene(parent, db)
        self.canvas.setSceneRect(0, 0, 10000, 10000)
        self.setScene(self.canvas)
        self.centerOn(0, 0)


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent, db):
        super(GraphicsScene, self).__init__(parent=parent)
        self.scene = Scene(db)
        self.parent = parent

    def mouseMoveEvent(self, event):
        self.parent.status_bar.showMessage('(' + str(event.scenePos().x()) + ' , ' + str(event.scenePos().y()) + ')')
        super(GraphicsScene, self).mouseMoveEvent(event)

    def add_merging_conflict(self):
        self.scene.clear()
        self.clear()
        self._add_roads('m ')

    def add_diverging_conflict(self):
        self.scene.clear()
        self.clear()
        self._add_roads('d ')

    def add_crossing_conflict(self):
        self.scene.clear()
        self.clear()
        self._add_roads('c ')

    def add_t_intersection(self):
        self.scene.clear()
        self.clear()
        self._add_roads('t ')

    def add_y_intersection(self):
        self.scene.clear()
        self.clear()
        self._add_roads('y ')

    def add_roundabout(self):
        self.scene.clear()
        self.clear()

        self._add_roads('r ')

    def add_four_legged(self):
        self.scene.clear()
        self.clear()
        self._add_roads('f ')

    def _add_roads(self, identifier):
        for link_label in self.scene.db['roads']['links']:
            if link_label.startswith(identifier):
                link = self.scene.db['roads']['links'][link_label]
                self.scene.add_link(link)

                dlink = factory.create_dlink(link)
                self.addItem(dlink)

        for conn_label in self.scene.db['roads']['connectors']:
            if conn_label.startswith(identifier):
                conn = self.scene.db['roads']['connectors'][conn_label]
                self.scene.add_connector(conn)

                dconn = factory.create_dconnector(conn)
                self.addItem(dconn)

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
