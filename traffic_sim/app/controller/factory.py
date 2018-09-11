from app.model.infra.node import Node
from app.model.infra.road import Link, Connector
from app.view.drawables.dnode import DNode
from app.view.drawables.droad import DLink, DConnector


def create_node(x, y, dir_):
    return Node(x, y, dir_)


def create_link(label, src_x, src_y, dst_x, dst_y, lanes):
    src = create_node(src_x, src_y, 'src')
    dst = create_node(dst_x, dst_y, 'dst')

    return Link(label, src, dst, lanes)


def create_connector(label, src_road, dst_road):
    return Connector(label, src_road, dst_road)


def create_dnode(node):
    return DNode(node)


def create_dlink(link):
    return DLink(link)


def create_dconnector(connector):
    return DConnector(connector)
