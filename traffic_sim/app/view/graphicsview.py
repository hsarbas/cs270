from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from app.model.scene import Scene
from app.controller import factory


class GraphicsView(QGraphicsView):
    """
    Serves as a window to enable user to see and visualize contents of GraphicsScene
    Inherits QGraphicsView
    """

    def __init__(self, parent, db):
        """
        Initialize GraphicsView

        :param parent: app object
        :param db: database object
        """

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
    """
    Serves as container for all drawable objects used in a simulation
    Inherits QGraphicsScene
    """

    def __init__(self, parent, db):
        """
        Initialize GraphicsScene

        :param parent: app object
        :param db: database object
        """

        super(GraphicsScene, self).__init__(parent=parent)
        self.scene = Scene(db)
        self.parent = parent

    def mouseMoveEvent(self, event):
        """
        Respond to mouse movement
        Update status bar to display x and y coordinates under current mouse position

        :param event: mouse event
        """

        self.parent.status_bar.showMessage('(' + str(event.scenePos().x()) + ' , ' + str(event.scenePos().y()) + ')')
        super(GraphicsScene, self).mouseMoveEvent(event)

    def add_merging_conflict(self):
        """
        Add necessary road network objects for merging conflict
        """

        self.scene.clear()
        self.clear()
        self._add_roads('m ')

    def add_diverging_conflict(self):
        """
        Add necessary road network objects for diverging conflict
        """

        self.scene.clear()
        self.clear()
        self._add_roads('d ')

    def add_crossing_conflict(self):
        """
        Add necessary road network objects for crossing conflict
        """

        self.scene.clear()
        self.clear()
        self._add_roads('c ')

    def add_t_intersection(self):
        """
        Add necessary road network objects for t-intersection
        """

        self.scene.clear()
        self.clear()
        self._add_roads('t ')

    def add_y_intersection(self):
        """
        Add necessary road network objects for y-intersection
        """

        self.scene.clear()
        self.clear()
        self._add_roads('y ')

    def add_roundabout(self):
        """
        Add necessary road network objects for roundabout
        """

        self.scene.clear()
        self.clear()

        self._add_roads('r ')

    def add_four_legged(self):
        """
        Add necessary road network objects for four-legged intersection
        """

        self.scene.clear()
        self.clear()
        self._add_roads('f ')

    def _add_roads(self, identifier):
        """
        Add necessary road network objects based of given identifier

        :param identifier: conflict/intersection identifier (string)
        """

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
        """
        Create DAgent object and add to canvas

        :param agent: Agent object
        """

        if agent:
            dagent = factory.create_dagent(self, agent)
            self.addItem(dagent)

    def remove_dagent(self, dagent):
        """
        Remove and delete DAgent from canvas
        :param dagent: DAgent object
        """

        self.removeItem(dagent)
        del dagent

    def recolor(self, run=True):
        """
        Recolor DLink to LightGray(DarkGray) if simulation is running(paused/stopped)
        :param run: simulation is running or stopped (boolean)
        """

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
