from app.model.infra.node import Node
from app.model.infra.road import Link, Connector
from app.model.meta.traffic import Dispatcher
from app.model.agent.agent import Agent
from app.view.drawables.dnode import DNode
from app.view.drawables.droad import DLink, DConnector
from app.view.drawables.dagent import DAgent


def create_node(x, y, dir_):
    return Node(x, y, dir_)


def create_link(label, src_x, src_y, dst_x, dst_y, lanes):
    src = create_node(src_x, src_y, 'src')
    dst = create_node(dst_x, dst_y, 'dst')

    return Link(label, src, dst, lanes)


def create_connector(label, src_road, dst_road, conflict_groups):
    return Connector(label, src_road, dst_road, conflict_groups)


def create_dispatcher(road, agent_manager):
    return Dispatcher(road, agent_manager)


def create_dnode(node):
    return DNode(node)


def create_dlink(link):
    return DLink(link)


def create_dconnector(connector):
    return DConnector(connector)


def create_agent(vel, acc, route):
    return Agent(vel, acc, route)


def create_dagent(gc, agent):
    return DAgent(gc, agent)
