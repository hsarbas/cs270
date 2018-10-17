from PySide2.QtCore import *
import weakref
from app.utils import tools


class AbstractObserver(QObject):
    def __init__(self, agent_manager):
        super(AbstractObserver, self).__init__(parent=None)

        self._agent_manager = weakref.ref(agent_manager)
        self._clock = weakref.ref(agent_manager.clock)

    @property
    def agent_manager(self):
        return self._agent_manager()

    @property
    def clock(self):
        return self._clock()


class AgentCounter(AbstractObserver):
    def __init__(self, agent_manager):
        super(AgentCounter, self).__init__(agent_manager)

        self.created = 0
        self.deleted = 0
        self.active = 0

        self.agent_manager.agent_created.connect(self.count_new_agent)
        self.agent_manager.agent_deleted.connect(self.count_deleted_agent)

    def count_new_agent(self):
        self.created += 1
        self.active += 1

    def count_deleted_agent(self):
        self.deleted += 1
        self.active -= 1

    def reset(self):
        self.created = 0
        self.deleted = 0
        self.active = 0


class TimeSpeedObserver(AbstractObserver):
    def __init__(self, agent_manager):
        super(TimeSpeedObserver, self).__init__(agent_manager)

        self.ave_speed = 0.0
        self.ave_time = 0.0

        self.clock.fine.connect(self.compute_ave_speed)

    def compute_ave_speed(self):
        total_speed = 0
        total_time = 0
        num_agents = len(self.agent_manager.agents)

        if num_agents:
            for agent in self.agent_manager.agents:
                total_speed += agent.vel
                total_time += agent.time_active

            self.ave_speed = tools.mps_to_kph(total_speed / num_agents)
            self.ave_time = total_time / num_agents

    def reset(self):
        self.ave_speed = 0
        self.ave_time = 0
