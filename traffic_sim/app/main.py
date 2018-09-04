import sys
from PySide2.QtWidgets import *


class TrafficSim(QMainWindow):
    def __init__(self, parent):
        super(TrafficSim, self).__init__()
        self.parent = parent

        self.setWindowTitle('CS270 Final Project - Traffic Simulator')
        self.setGeometry(400, 100, 1080, 720)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    _ = TrafficSim(app)
    sys.exit(app.exec_())
