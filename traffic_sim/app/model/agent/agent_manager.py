from PySide2.QtCore import *
import weakref
import collections
import transaction
from app.utils import const


class AgentManager(QObject):

    agent_created = Signal()
    agent_moved = Signal()

    def __init__(self, db, clock):
        super(AgentManager, self).__init__(parent=None)
        self.agents = db['agents']
        self.clock = clock
        self._road_index = collections.defaultdict(list)

    def add_agent(self, agent, road, pos, lane):
        self.agents[agent] = (road, pos, lane)
        self._road_index[road].append(agent)
        self.agent_created.emit()

        transaction.commit()

    def move_agent(self, agent):
        acc = agent.deliberate_acc()
        new_vel = round(agent.vel + acc * (const.DT/100), 2)
        agent.vel = new_vel
        agent.acc = acc

        transaction.commit()

    def step(self):
        for agent in self.agents:
            self.move_agent(agent)
