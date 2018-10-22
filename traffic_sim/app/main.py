import os
import sys

import ZODB
import ZODB.FileStorage
import transaction
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from persistent.mapping import PersistentMapping

from app.controller import factory
from app.view.dock_widgets.toolboxdockwidget import ToolBoxDockWidget
from app.view.dock_widgets.resultsdockwidget import ResultsDockWidget
from app.view.graphicsview import GraphicsView
from app.model.simulator import Engine


class TrafficSim(QMainWindow):
    def __init__(self, parent):
        super(TrafficSim, self).__init__()
        self.parent = parent

        self.menu_bar = self.menuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.toolbar = QToolBar('Toolbar', parent=self)
        self.addToolBar(self.toolbar)
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.toolbox = None
        self.results = None
        self.gc = None
        self.db_root = None
        self.db_connection = None

        self._initialize_db()
        self._populate_db()
        self._initialize_ui()

        self.simulator = Engine(self, self.gc)

        self.show()

    def _initialize_ui(self):
        self.setWindowTitle('CS270 Final Project - Traffic Simulator')

        icons_dir = os.path.join(os.path.dirname(__file__), 'view/icons/toolbar icons')

        clear_map_action = QAction('&Clear map...', self)
        icon = QIcon(os.path.join(icons_dir, 'clear map.png'))
        clear_map_action.setIcon(icon)
        clear_map_action.setShortcut('Ctrl+C')
        clear_map_action.setStatusTip('Clear map')
        clear_map_action.triggered.connect(self.clear_map)

        quit_action = QAction('&Quit simulator...', self)
        icon = QIcon(os.path.join(icons_dir, 'quit.png'))
        quit_action.setIcon(icon)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Quit simulator')
        quit_action.triggered.connect(self.close)

        file_menu = QMenu('&File')
        file_menu.addAction(clear_map_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)
        self.menu_bar.addMenu(file_menu)

        zoom_in_action = QAction('Zoom in', self)
        icon = QIcon(os.path.join(icons_dir, 'zoom in.png'))
        zoom_in_action.setIcon(icon)
        zoom_in_action.setShortcut('Ctrl+]')
        zoom_in_action.setStatusTip('Zoom in')
        zoom_in_action.triggered.connect(self.zoom_in)

        zoom_out_action = QAction('Zoom out', self)
        icon = QIcon(os.path.join(icons_dir, 'zoom out.png'))
        zoom_out_action.setIcon(icon)
        zoom_out_action.setShortcut('Ctrl+[')
        zoom_out_action.setStatusTip('Zoom out')
        zoom_out_action.triggered.connect(self.zoom_out)

        zoom_to_fit_action = QAction('Zoom to fit', self)
        icon = QIcon(os.path.join(icons_dir, 'zoom fit.png'))
        zoom_to_fit_action.setIcon(icon)
        zoom_to_fit_action.setShortcut('Ctrl+\\')
        zoom_to_fit_action.setStatusTip('Zoom to fit')
        zoom_to_fit_action.triggered.connect(self.zoom_to_fit)

        view_menu = QMenu('&View')
        view_menu.addAction(zoom_in_action)
        view_menu.addAction(zoom_out_action)
        view_menu.addAction(zoom_to_fit_action)
        self.menu_bar.addMenu(view_menu)

        parameters_action = QAction('&Parameters...', self)
        icon = QIcon(os.path.join(icons_dir, 'parameters.png'))
        parameters_action.setIcon(icon)
        parameters_action.setShortcut('Ctrl+P')
        parameters_action.setStatusTip('Open simulation parameters')
        parameters_action.triggered.connect(self.open_simulation_parameters)

        run_action = QAction('&Run', self)
        icon = QIcon(os.path.join(icons_dir, 'run.png'))
        run_action.setIcon(icon)
        run_action.setShortcut('Ctrl+R')
        run_action.setStatusTip('Run simulation')
        run_action.triggered.connect(self.run)

        pause_action = QAction('Pause', self)
        icon = QIcon(os.path.join(icons_dir, 'pause.png'))
        pause_action.setIcon(icon)
        pause_action.setShortcut('Ctrl+A')
        pause_action.setStatusTip('Pause current simulation')
        pause_action.triggered.connect(self.pause)

        stop_action = QAction('&Stop', self)
        icon = QIcon(os.path.join(icons_dir, 'stop.png'))
        stop_action.setIcon(icon)
        stop_action.setShortcut('Ctrl+S')
        stop_action.setStatusTip('Stop current simulation')
        stop_action.triggered.connect(self.stop)

        traffic_data_menu = QMenu('&Simulation')
        traffic_data_menu.addAction(parameters_action)
        traffic_data_menu.addSeparator()
        traffic_data_menu.addAction(run_action)
        traffic_data_menu.addAction(pause_action)
        traffic_data_menu.addAction(stop_action)
        self.menu_bar.addMenu(traffic_data_menu)

        self.toolbar.addAction(clear_map_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(parameters_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(zoom_in_action)
        self.toolbar.addAction(zoom_out_action)
        self.toolbar.addAction(zoom_to_fit_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(run_action)
        self.toolbar.addAction(pause_action)
        self.toolbar.addAction(stop_action)

        self.gc = GraphicsView(self, self.db_root)
        self.setCentralWidget(self.gc)

        self.toolbox = ToolBoxDockWidget(self, self.gc)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.toolbox)

        self.results = ResultsDockWidget(self, self.gc)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.results)

    def _initialize_db(self):

        if os.name == 'posix':
            _db_dir = os.path.join(os.path.dirname(__file__), 'model/db/simulator.fs')
        else:
            _db_dir = os.path.join(os.path.dirname(__file__), 'model\db\simulator.fs')

        # print _db_dir
        storage = ZODB.FileStorage.FileStorage(_db_dir)
        # storage = ZODB.FileStorage.FileStorage('simulator.fs')
        _db = ZODB.DB(storage)

        self.db_connection = _db.open()
        self.db_root = self.db_connection.root()

        if 'roads' not in self.db_root:
            self.db_root['roads'] = PersistentMapping()
            self.db_root['roads']['links'] = PersistentMapping()
            self.db_root['roads']['connectors'] = PersistentMapping()
            transaction.commit()

    def _populate_db(self):
        self._populate_merging()
        self._populate_diverging()
        self._populate_crossing()
        self._populate_t_intersection()
        self._populate_y_intersection()
        self._populate_roundabout()
        self._populate_four_legged()

    def _populate_merging(self):
        link_1 = factory.create_link('m link 1', 100, 100, 590, 100, 2)
        link_2 = factory.create_link('m link 2', 650, 100, 1000, 100, 2)
        link_3 = factory.create_link('m link 3', 200, 300, 600, 125, 2)

        conn_1_2 = factory.create_connector('m conn 1', link_1, link_2, [1])  # conn_from_to
        conn_3_2 = factory.create_connector('m conn 2', link_3, link_2, [1])

        self.db_root['roads']['links'][link_1.label] = link_1
        self.db_root['roads']['links'][link_2.label] = link_2
        self.db_root['roads']['links'][link_3.label] = link_3

        self.db_root['roads']['connectors'][conn_1_2.label] = conn_1_2
        self.db_root['roads']['connectors'][conn_3_2.label] = conn_3_2

        transaction.commit()

    def _populate_diverging(self):
        link_1 = factory.create_link('d link 1', 100, 100, 500, 100, 2)
        link_2 = factory.create_link('d link 2', 560, 100, 1000, 100, 2)
        link_3 = factory.create_link('d link 3', 560, 160, 930, 350, 2)

        conn_1_2 = factory.create_connector('d conn 1', link_1, link_2, [1])  # conn_from_to
        conn_1_3 = factory.create_connector('d conn 2', link_1, link_3, [1])

        self.db_root['roads']['links'][link_1.label] = link_1
        self.db_root['roads']['links'][link_2.label] = link_2
        self.db_root['roads']['links'][link_3.label] = link_3

        self.db_root['roads']['connectors'][conn_1_2.label] = conn_1_2
        self.db_root['roads']['connectors'][conn_1_3.label] = conn_1_3

        transaction.commit()

    def _populate_crossing(self):
        pass

    def _populate_t_intersection(self):
        pass

    def _populate_y_intersection(self):
        pass

    def _populate_roundabout(self):
        link_1 = factory.create_link('r link 1', 50, 320, 250, 320, 2)
        link_2 = factory.create_link('r link 2', 290, 350, 380, 450, 2)
        link_3 = factory.create_link('r link 3', 400, 495, 400, 650, 2)
        link_4 = factory.create_link('r link 4', 440, 650, 440, 495, 2)
        link_5 = factory.create_link('r link 5', 460, 450, 550, 350, 2)
        link_6 = factory.create_link('r link 6', 590, 320, 770, 320, 2)
        link_7 = factory.create_link('r link 7', 770, 280, 590, 280, 2)
        link_8 = factory.create_link('r link 8', 550, 260, 460, 190, 2)
        link_9 = factory.create_link('r link 9', 440, 140, 440, 10, 2)
        link_10 = factory.create_link('r link 10', 400, 10, 400, 140, 2)
        link_11 = factory.create_link('r link 11', 390, 190, 290, 270, 2)
        link_12 = factory.create_link('r link 12', 250, 280, 50, 280, 2)

        conn_1_2 = factory.create_connector('r conn 1', link_1, link_2, [1])
        conn_2_3 = factory.create_connector('r conn 2', link_2, link_3, [2])
        conn_4_5 = factory.create_connector('r conn 3', link_4, link_5, [3])
        conn_2_5 = factory.create_connector('r conn 4', link_2, link_5, [2, 3])
        conn_5_6 = factory.create_connector('r conn 5', link_5, link_6, [4])
        conn_7_8 = factory.create_connector('r conn 6', link_7, link_8, [5])
        conn_5_8 = factory.create_connector('r conn 7', link_5, link_8, [4, 5])
        conn_8_9 = factory.create_connector('r conn 8', link_8, link_9, [6])
        conn_10_11 = factory.create_connector('r conn 9', link_10, link_11, [7])
        conn_8_11 = factory.create_connector('r conn 10', link_8, link_11, [6, 7])
        conn_11_12 = factory.create_connector('r conn 11', link_11, link_12, [8])
        conn_11_2 = factory.create_connector('r conn 12', link_11, link_2, [1, 8])

        self.db_root['roads']['links'][link_1.label] = link_1
        self.db_root['roads']['links'][link_2.label] = link_2
        self.db_root['roads']['links'][link_3.label] = link_3
        self.db_root['roads']['links'][link_4.label] = link_4
        self.db_root['roads']['links'][link_5.label] = link_5
        self.db_root['roads']['links'][link_6.label] = link_6
        self.db_root['roads']['links'][link_7.label] = link_7
        self.db_root['roads']['links'][link_8.label] = link_8
        self.db_root['roads']['links'][link_9.label] = link_9
        self.db_root['roads']['links'][link_10.label] = link_10
        self.db_root['roads']['links'][link_11.label] = link_11
        self.db_root['roads']['links'][link_12.label] = link_12

        self.db_root['roads']['connectors'][conn_1_2.label] = conn_1_2
        self.db_root['roads']['connectors'][conn_2_3.label] = conn_2_3
        self.db_root['roads']['connectors'][conn_4_5.label] = conn_4_5
        self.db_root['roads']['connectors'][conn_2_5.label] = conn_2_5
        self.db_root['roads']['connectors'][conn_5_6.label] = conn_5_6
        self.db_root['roads']['connectors'][conn_7_8.label] = conn_7_8
        self.db_root['roads']['connectors'][conn_5_8.label] = conn_5_8
        self.db_root['roads']['connectors'][conn_8_9.label] = conn_8_9
        self.db_root['roads']['connectors'][conn_10_11.label] = conn_10_11
        self.db_root['roads']['connectors'][conn_8_11.label] = conn_8_11
        self.db_root['roads']['connectors'][conn_11_12.label] = conn_11_12
        self.db_root['roads']['connectors'][conn_11_2.label] = conn_11_2
        transaction.commit()

    def _populate_four_legged(self):
        pass

    def _close_db(self):
        if self.db_connection:
            self.db_connection.close()

    def _delete_db(self):
        if os.name == 'posix':
            _db_dir = os.path.join(os.path.dirname(__file__), 'model/db/')
        else:
            _db_dir = os.path.join(os.path.abspath(__file__), 'model\\db\\')

        for root, dirs, files in os.walk(_db_dir):
            for file_ in files:
                os.remove(os.path.join(root, file_))

    def clear_map(self):
        pass

    def open_simulation_parameters(self):
        pass
    
    def run(self):
        self.simulator.play()

    def pause(self):
        self.simulator.pause()

    def stop(self):
        self.simulator.stop()

    def zoom_in(self):
        self.gc.scale(1.1, 1.1)

    def zoom_out(self):
        self.gc.scale(0.9, 0.9)

    def zoom_to_fit(self):
        transform = QTransform(1.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000)

        self.gc.setTransform(transform)
        self.gc.fitInView(self.gc.canvas.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.gc.ensureVisible(self.gc.canvas.itemsBoundingRect())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit simulator',
                                           "Are you sure to close the app?", QMessageBox.Yes |
                                           QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self._close_db()
            self._delete_db()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')

    _ = TrafficSim(app)
    sys.exit(app.exec_())
