from app.model.infra.node import Node
from app.model.infra.road import Link, Connector
from app.view.drawables.droad import DLink


def create_node(x, y, dir_):
    return Node(x, y, dir_)


def create_link(src_x, src_y, dst_x, dst_y, lanes):
    src = create_node(src_x, src_y, 'src')
    dst = create_node(dst_x, dst_y, 'dst')

    return Link(src, dst, lanes)


def create_connector(src_road, dst_road):
    return Connector(src_road, dst_road)


def create_dlink(link):
    return DLink(link)
