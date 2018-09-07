import sys
import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from app.view.dock_widgets.toolboxdockwidget import ToolBoxDockWidget
from app.view.graphicsview import GraphicsView


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
        self.gc = None

        self._initialize_ui()

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

        file_menu = QMenu('File')
        file_menu.addAction(clear_map_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)
        self.menu_bar.addMenu(file_menu)

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

        traffic_data_menu = QMenu('Simulation')
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
        self.toolbar.addAction(run_action)
        self.toolbar.addAction(pause_action)
        self.toolbar.addAction(stop_action)

        self.gc = GraphicsView(self)
        self.setCentralWidget(self.gc)

        self.toolbox = ToolBoxDockWidget(self, self.gc)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.toolbox)

    def clear_map(self):
        pass

    def open_simulation_parameters(self):
        pass
    
    def run(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit simulator',
                                           "Are you sure to close the app?", QMessageBox.Yes |
                                           QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')

    _ = TrafficSim(app)
    sys.exit(app.exec_())
