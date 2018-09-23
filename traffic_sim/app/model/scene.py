class Scene(object):
    def __init__(self, db):
        self.db = db
        self.links = []
        self.connectors = []

    def add_link(self, link):
        self.links.append(link)

    def add_connector(self, connector):
        self.connectors.append(connector)

    def populate_scene(self):
        pass

    def clear(self):
        self.links = []
        self.connectors = []
