from app.utils.clock import Clock
from PySide2.QtCore import *


class Engine(QObject):
    def __init__(self, parent, scene):
        super(Engine, self).__init__(parent=parent)
        self.parent = parent
        self.clock = Clock()
        self.clock.coarse.connect(self._step)
        self.scene = scene

    def _step(self, time):
        self.parent.status_bar.showMessage(str(time))

    def play(self):
        for dispatcher in self.scene.dispatchers.values():
            dispatcher.run(self.clock)
            dispatcher.dispatch_agent.connect(self.agent_dispatched_callback)

        self.clock.run()

    def pause(self):
        self.clock.pause()

    def stop(self):
        self.clock.reset()

    def agent_dispatched_callback(self):
        print 'agent_dispatched!'
