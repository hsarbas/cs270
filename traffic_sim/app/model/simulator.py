from app.utils.clock import Clock
from app.model.agent.agent_manager import AgentManager
from PySide2.QtCore import *
from app.controller import factory
import networkx as nx
import random
import copy


class Engine(QObject):
    def __init__(self, parent, gc):
        super(Engine, self).__init__(parent=parent)
        self.parent = parent
        self.clock = Clock()
        self.clock.fine.connect(self.step)
        self.clock.coarse.connect(self.update_timer)
        self.gc = gc
        self.scene = gc.canvas.scene
        self.agent_manager = AgentManager(self.scene, self.clock)
        self.graph = None

    def update_timer(self, time):
        self.parent.status_bar.showMessage(str(time))

    def step(self):
        self.agent_manager.step()

    def play(self):
        self.convert_to_networkx_graph()

        for link_label in self.scene.entry_roads:
            # if link_label in ['link 1']:
            #     link = self.scene.links[link_label]
            #     dispatcher = factory.create_dispatcher(link)
            #     self.scene.add_dispatcher(dispatcher)
            #
            #     dispatcher.run(self.clock)
            #     dispatcher.dispatch_agent.connect(self.agent_dispatched_callback)
            link = self.scene.links[link_label]
            dispatcher = factory.create_dispatcher(link)
            self.scene.add_dispatcher(dispatcher)

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

        route = self.random_route(road.label)

        agent = factory.create_agent(init_vel, init_acc, copy.deepcopy(route))
        agent.route.pop(0)  # remove first road

        self.agent_manager.add_agent(agent, road, pos, lane)
        self.gc.canvas.add_dagent(agent)

    def convert_to_networkx_graph(self):
        connectors = self.scene.connectors
        self.graph = nx.DiGraph()

        for connector in connectors.values():
            src_road = connector.src_road.label
            dst_road = connector.dst_road.label

            dist_src = connector.src_road.length
            dist_dst = connector.dst_road.length

            self.graph.add_edge(src_road, connector.label, dist=dist_src)
            self.graph.add_edge(connector.label, dst_road, dist=dist_dst)

        for node in self.graph.nodes():
            if self.graph.in_degree(node) == 0:
                self.scene.entry_roads.append(node)

            if self.graph.out_degree(node) == 0:
                self.scene.exit_roads.append(node)

        for entry_road in self.scene.entry_roads:
            for exit_road in self.scene.exit_roads:
                for route in nx.all_simple_paths(self.graph, entry_road, exit_road):
                    self.scene.routes[entry_road].append(route)

    def random_route(self, road_label):
        return random.choice(self.scene.routes[road_label])
