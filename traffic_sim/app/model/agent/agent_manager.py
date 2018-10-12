from PySide2.QtCore import *
import weakref
import collections
from app.utils import const


class AgentManager(QObject):

    agent_created = Signal()  # for observer class
    agent_moved = Signal()  # for observer class

    def __init__(self, scene, clock):
        super(AgentManager, self).__init__(parent=None)
        self.agents = weakref.WeakKeyDictionary()
        self.scene = scene
        self.clock = clock
        self._road_index = collections.defaultdict(list)

    def add_agent(self, agent, road, pos, lane):
        self.agents[agent] = (road, pos, lane)
        self._road_index[road].append(agent)
        self.agent_created.emit()

    def remove_agent(self, agent):
        road, _, _ = self.agents[agent]
        self._road_index[road].remove(agent)
        del self.agents[agent]

    def move_agent(self, agent):
        road, pos, lane = self.agents[agent]

        new_acc = agent.deliberate_acc()
        new_vel = round(agent.vel + new_acc * (const.DT/100), 2)
        new_pos = round(pos + new_vel * (const.DT/100), 2)

        if new_pos > road.length:

            try:
                new_road_label = agent.route.pop(0)
                new_road = self.scene.links[new_road_label] if new_road_label in self.scene.links \
                    else self.scene.connectors[new_road_label]

                self._road_index[road].remove(agent)
                self._road_index[new_road].append(agent)

            except IndexError:
                self.remove_agent(agent)
                new_road = None

            new_pos = 0.0
        else:
            new_road = road

        new_lane = lane

        if new_road:
            agent.move(new_vel, new_acc, new_road, new_pos, new_lane)
            self.agents[agent] = (new_road, new_pos, new_lane)

    def step(self):
        for agent in list(self.agents):
            self.move_agent(agent)
