import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ToolBoxDockWidget(QDockWidget):
    def __init__(self, parent, gc):
        super(ToolBoxDockWidget, self).__init__(parent=parent)
        self.setWindowTitle('Toolbox')
        self.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
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

        main_layout = QGridLayout(self)
        groupbox = QGroupBox()

        main_layout.addWidget(groupbox)
        btn_layout = QGridLayout(groupbox)

        merging_btn = QToolButton()
        merging_btn.setText('Merging conflict')
        merging_btn.setStatusTip('Create a simple merging conflict')
        merging_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        diverging_btn = QToolButton()
        diverging_btn.setText('Diverging conflict')
        diverging_btn.setStatusTip('Create a simple diverging conflict')
        diverging_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        crossing_btn = QToolButton()
        crossing_btn.setText('Crossing conflict')
        crossing_btn.setStatusTip('Create a simple crossing conflict')
        crossing_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        btn_layout.addWidget(merging_btn, 0, 0)
        btn_layout.addWidget(diverging_btn, 1, 0)
        btn_layout.addWidget(crossing_btn, 2, 0)


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

        y_intersection_btn = QToolButton()
        y_intersection_btn.setText('Y intersection')
        y_intersection_btn.setStatusTip('Create a Y intersection')
        y_intersection_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        roundabout_btn = QToolButton()
        roundabout_btn.setText('Roundabout')
        roundabout_btn.setStatusTip('Create a roundabout')
        roundabout_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        four_leg_intersection = QToolButton()
        four_leg_intersection.setText('4-legged intersection')
        four_leg_intersection.setStatusTip('Create a 4-legged intersection')
        four_leg_intersection.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        btn_layout.addWidget(t_intersection_btn, 0, 0)
        btn_layout.addWidget(y_intersection_btn, 1, 0)
        btn_layout.addWidget(roundabout_btn, 2, 0)
        btn_layout.addWidget(four_leg_intersection, 3, 0)
