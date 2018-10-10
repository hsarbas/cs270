from PySide2.QtCore import *
import weakref
import collections
from app.utils import const


class AgentManager(QObject):

    agent_created = Signal()  # for observer class
    agent_moved = Signal()  # for observer class

    def __init__(self, clock):
        super(AgentManager, self).__init__(parent=None)
        self.agents = weakref.WeakKeyDictionary()
        self.clock = clock
        self._road_index = collections.defaultdict(list)

    def add_agent(self, agent, road, pos, lane):
        self.agents[agent] = (road, pos, lane)
        self._road_index[road].append(agent)
        self.agent_created.emit()

    def move_agent(self, agent):
        road, pos, lane = self.agents[agent]

        new_acc = agent.deliberate_acc()
        new_vel = round(agent.vel + new_acc * (const.DT/100), 2)

        new_road = road
        new_pos = round(pos + new_vel * (const.DT/100), 2)
        new_lane = lane

        agent.move(new_vel, new_acc, new_road, new_pos, new_lane)

        self.agents[agent] = (new_road, new_pos, new_lane)

    def step(self):
        for agent in self.agents:
            self.move_agent(agent)
