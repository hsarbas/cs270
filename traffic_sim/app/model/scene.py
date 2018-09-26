import weakref


class Scene(object):
    def __init__(self, db):
        self.db = db
        self.links = []
        self.connectors = []
        self.dispatchers = weakref.WeakKeyDictionary()

    def add_link(self, link):
        self.links.append(link)

    def add_connector(self, connector):
        self.connectors.append(connector)

    def add_dispatcher(self, dispatcher):
        self.dispatchers[dispatcher.road] = dispatcher

    def populate_scene(self):
        pass

    def clear(self):
        self.links = []
        self.connectors = []
        self.dispatchers.clear()
