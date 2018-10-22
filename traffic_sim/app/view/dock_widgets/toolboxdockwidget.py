import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ToolBoxDockWidget(QDockWidget):
    def __init__(self, parent, gc):
        super(ToolBoxDockWidget, self).__init__(parent=parent)
        self.setWindowTitle('Toolbox')
        # self.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        self.setFloating(False)
        self.parent = parent
        self.gc = gc

        self.toolbox = QToolBox(parent=parent)
        self.setWidget(self.toolbox)

        self.conflict_types = ConflictTypes(gc, parent)
        self.intersection_types = IntersectionTypes(gc, parent)

        self.toolbox.addItem(self.conflict_types, 'Conflict types')
        self.toolbox.addItem(self.intersection_types, 'Intersection types')

        icons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons/toolbox icons')

        icon = QIcon(os.path.join(icons_dir, 'conflicts.png'))
        self.toolbox.setItemIcon(0, icon)

        icon = QIcon(os.path.join(icons_dir, 'intersections.png'))
        self.toolbox.setItemIcon(1, icon)


class ConflictTypes(QWidget):
    def __init__(self, gc, parent):
        super(ConflictTypes, self).__init__(parent=parent)
        self.gc = gc
        self.parent = parent

        icons_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons/toolbox icons')

        main_layout = QGridLayout(self)
        groupbox = QGroupBox()

        main_layout.addWidget(groupbox)
        btn_layout = QGridLayout(groupbox)

        merging_btn = QToolButton()
        merging_btn.setText('Merging conflict')
        merging_btn.setStatusTip('Create a simple merging conflict')
        merging_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        icon = QIcon(os.path.join(icons_dir, 'merging.png'))
        merging_btn.setIcon(icon)
        merging_btn.clicked.connect(self.merging_btn_clicked)

        diverging_btn = QToolButton()
        diverging_btn.setText('Diverging conflict')
        diverging_btn.setStatusTip('Create a simple diverging conflict')
        diverging_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        icon = QIcon(os.path.join(icons_dir, 'diverging.png'))
        diverging_btn.setIcon(icon)
        diverging_btn.clicked.connect(self.diverging_btn_clicked)

        crossing_btn = QToolButton()
        crossing_btn.setText('Crossing conflict')
        crossing_btn.setStatusTip('Create a simple crossing conflict')
        crossing_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        crossing_btn.clicked.connect(self.crossing_btn_clicked)

        btn_layout.addWidget(merging_btn, 0, 0)
        btn_layout.addWidget(diverging_btn, 1, 0)
        btn_layout.addWidget(crossing_btn, 2, 0)

    def merging_btn_clicked(self):
        self.gc.canvas.add_merging_conflict()

    def diverging_btn_clicked(self):
        self.gc.canvas.add_diverging_conflict()

    def crossing_btn_clicked(self):
        self.gc.canvas.add_crossing_conflict()


class IntersectionTypes(QWidget):
    def __init__(self, gc, parent):
        super(IntersectionTypes, self).__init__(parent=parent)
        self.gc = gc
        self.parent = parent

        main_layout = QGridLayout(self)
        groupbox = QGroupBox()

        main_layout.addWidget(groupbox)
        btn_layout = QGridLayout(groupbox)

        t_intersection_btn = QToolButton()
        t_intersection_btn.setText('T intersection')
        t_intersection_btn.setStatusTip('Create a T intersection')
        t_intersection_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        t_intersection_btn.clicked.connect(self.t_intersection_btn_clicked)

        y_intersection_btn = QToolButton()
        y_intersection_btn.setText('Y intersection')
        y_intersection_btn.setStatusTip('Create a Y intersection')
        y_intersection_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        y_intersection_btn.clicked.connect(self.y_intersection_btn_clicked)

        roundabout_btn = QToolButton()
        roundabout_btn.setText('Roundabout')
        roundabout_btn.setStatusTip('Create a roundabout')
        roundabout_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        roundabout_btn.clicked.connect(self.roundabout_btn_clicked)

        four_legged_btn = QToolButton()
        four_legged_btn.setText('4-legged intersection')
        four_legged_btn.setStatusTip('Create a 4-legged intersection')
        four_legged_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        four_legged_btn.clicked.connect(self.four_legged_btn_clicked)

        btn_layout.addWidget(t_intersection_btn, 0, 0)
        btn_layout.addWidget(y_intersection_btn, 1, 0)
        btn_layout.addWidget(roundabout_btn, 2, 0)
        btn_layout.addWidget(four_legged_btn, 3, 0)

    def t_intersection_btn_clicked(self):
        self.gc.canvas.add_t_intersection()

    def y_intersection_btn_clicked(self):
        self.gc.canvas.add_y_intersection()

    def roundabout_btn_clicked(self):
        self.gc.canvas.add_roundabout()

    def four_legged_btn_clicked(self):
        self.gc.canvas.add_four_legged()
