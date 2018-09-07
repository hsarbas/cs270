import sys
from PySide2.QtWidgets import *


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

        self._initialize_ui()

        self.show()

    def _initialize_ui(self):
        self.setWindowTitle('CS270 Final Project - Traffic Simulator')
        self.setGeometry(400, 100, 1080, 720)

        clear_map_action = QAction('&Clear map...', self)
        # icon = QIcon(os.path.join(icons_dir, 'new map.png'))
        # clear_map_action.setIcon(icon)
        clear_map_action.setShortcut('Ctrl+C')
        clear_map_action.setStatusTip('Clear map')
        clear_map_action.triggered.connect(self.clear_map)

        quit_action = QAction('&Quit simulator...', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Quit simulator')
        # icon = QIcon(os.path.join(icons_dir, 'quit.png'))
        # quit_action.setIcon(icon)
        quit_action.triggered.connect(self.close)

        file_menu = QMenu('File')
        file_menu.addAction(clear_map_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)
        self.menu_bar.addMenu(file_menu)

        traffic_data_action = QAction('&Traffic data...', self)
        traffic_data_action.setShortcut('Ctrl+T')
        traffic_data_action.setStatusTip('Open traffic data')
        traffic_data_action.triggered.connect(self.open_traffic_data)

        play_action = QAction('&Play', self)
        play_action.setShortcut('Ctrl+P')
        play_action.setStatusTip('Play simulation')
        play_action.triggered.connect(self.play)

        pause_action = QAction('Pause', self)
        pause_action.setShortcut('Ctrl+A')
        pause_action.setStatusTip('Pause current simulation')
        pause_action.triggered.connect(self.pause)

        stop_action = QAction('&Stop', self)
        stop_action.setShortcut('Ctrl+S')
        stop_action.setStatusTip('Stop current simulation')
        stop_action.triggered.connect(self.stop)

        traffic_data_menu = QMenu('Simulation')
        traffic_data_menu.addAction(traffic_data_action)
        traffic_data_menu.addSeparator()
        traffic_data_menu.addAction(play_action)
        traffic_data_menu.addAction(pause_action)
        traffic_data_menu.addAction(stop_action)
        self.menu_bar.addMenu(traffic_data_menu)

        self.toolbar.addAction(clear_map_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(traffic_data_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(play_action)
        self.toolbar.addAction(pause_action)
        self.toolbar.addAction(stop_action)

        self.status_bar.showMessage('status bar')

    def clear_map(self):
        pass

    def open_traffic_data(self):
        pass
    
    def play(self):
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
