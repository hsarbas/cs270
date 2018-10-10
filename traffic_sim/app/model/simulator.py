from app.utils.clock import Clock
from app.model.agent.agent import Agent
from app.model.agent.agent_manager import AgentManager
from PySide2.QtCore import *
from app.controller import factory


class Engine(QObject):
    def __init__(self, parent, gc):
        super(Engine, self).__init__(parent=parent)
        self.parent = parent
        self.clock = Clock()
        self.clock.fine.connect(self.step)
        self.clock.coarse.connect(self.update_timer)
        self.gc = gc
        self.scene = gc.canvas.scene
        self.agent_manager = AgentManager(self.clock)

    def update_timer(self, time):
        self.parent.status_bar.showMessage(str(time))

    def step(self):
        self.agent_manager.step()

    def play(self):
        for dispatcher in self.scene.dispatchers.values():
            dispatcher.run(self.clock)
            dispatcher.dispatch_agent.connect(self.agent_dispatched_callback)

        self.clock.run()

    def pause(self):
        self.clock.pause()

    def stop(self):
        self.clock.reset()

    def agent_dispatched_callback(self, init_val):

        init_vel = init_val['init_vel']
        init_acc = init_val['init_acc']

        road = init_val['road']
        pos = init_val['pos']
        lane = init_val['lane']

        agent = factory.create_agent(init_vel, init_acc)
        self.agent_manager.add_agent(agent, road, pos, lane)

        self.gc.canvas.add_dagent(agent)

