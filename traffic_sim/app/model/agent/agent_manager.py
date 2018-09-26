from PySide2.QtCore import *
import weakref
import collections


class AgentManager(QObject):

    agent_created = Signal()
    agent_moved = Signal()

    def __init__(self):
        super(AgentManager, self).__init__(parent=None)

        self.agents = weakref.WeakKeyDictionary()
        self._road_index = collections.defaultdict(list)

    def add_agent(self, agent, road, pos, lane):
        self.agents[agent] = (road, pos, lane)
        self._road_index[road].append(agent)
        self.agent_created.emit()

    def move_agent(self, agent, road, pos, lane):
        pass
