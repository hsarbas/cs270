import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ResultsDockWidget(QDockWidget):
    def __init__(self, parent, gc):
        super(ResultsDockWidget, self).__init__(parent=parent)
        self.setWindowTitle('Results')

        self.parent = parent
        self.gc = gc

        self.results_widget = QWidget()
        self.results_widget_layout = QGridLayout(self.results_widget)
        self.setWidget(self.results_widget)

        # agent counter results
        counter_results = QGroupBox('Agent counter')
        counter_results_layout = QGridLayout(counter_results)

        created_label = QLabel('Created:')
        deleted_label = QLabel('Deleted:')
        active_label = QLabel('Active:')

        self.created_input = QLineEdit()
        self.deleted_input = QLineEdit()
        self.active_input = QLineEdit()

        self.created_input.setEnabled(False)
        self.deleted_input.setEnabled(False)
        self.active_input.setEnabled(False)

        counter_results_layout.addWidget(created_label, 0, 0)
        counter_results_layout.addWidget(self.created_input, 0, 1)

        counter_results_layout.addWidget(deleted_label, 0, 2)
        counter_results_layout.addWidget(self.deleted_input, 0, 3)

        counter_results_layout.addWidget(active_label, 0, 4)
        counter_results_layout.addWidget(self.active_input, 0, 5)

        # measures of performance results
        performance = QGroupBox('Measures of performance')
        performance_layout = QGridLayout(performance)

        speed_label = QLabel('Average speed (kph):')
        time_label = QLabel('Average travel time (s):')

        self.speed_input = QLineEdit()
        self.time_input = QLineEdit()

        self.speed_input.setEnabled(False)
        self.time_input.setEnabled(False)

        performance_layout.addWidget(speed_label, 0, 0)
        performance_layout.addWidget(self.speed_input, 0, 1)
        performance_layout.addWidget(time_label, 0, 2)
        performance_layout.addWidget(self.time_input, 0, 3)

        self.results_widget_layout.addWidget(counter_results, 0, 0)
        self.results_widget_layout.addWidget(performance, 0, 1)
