import weakref
import collections


class Scene(object):
    def __init__(self, db):
        self.db = db
        self.links = weakref.WeakValueDictionary()
        self.connectors = weakref.WeakValueDictionary()
        self.dispatchers = weakref.WeakKeyDictionary()
        self.entry_roads = []
        self.exit_roads = []
        self.routes = collections.defaultdict(list)

    def add_link(self, link):
        self.links[link.label] = link

    def add_connector(self, connector):
        self.connectors[connector.label] = connector

    def add_dispatcher(self, dispatcher):
        self.dispatchers[dispatcher.road] = dispatcher

    def populate_scene(self):
        pass

    def clear(self):
        self.links.clear()
        self.connectors.clear()
        self.dispatchers.clear()
        self.entry_roads = []
        self.exit_roads = []
        self.routes.clear()

    def get_connector_by_conflict_group(self, group, conn):
        for connector in self.connectors.values():
            if conn != connector and group in connector.conflict_groups:
                return connector
