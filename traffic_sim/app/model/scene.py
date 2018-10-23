import weakref
import collections


class Scene(object):
    """
    Serves as container for all (non-drawable) objects used in a simulation
    """

    def __init__(self, db):
        """
        Initialize Scene

        :param db: database object

        links: dictionary of link objects; links[link.label] = link
        connectors: dictionary of connector objects; connectors[connector.label] = connector
        dispatchers: dictionary of dispatcher objects; dispatcher[dispatcher.road] = dispatcher
        entry_roads: list of entry roads in a network
        exit_roads: list of exit roads in a network
        routes: dictionary of routes
        """

        self.db = db
        self.links = weakref.WeakValueDictionary()
        self.connectors = weakref.WeakValueDictionary()
        self.dispatchers = weakref.WeakKeyDictionary()
        self.entry_roads = []
        self.exit_roads = []
        self.routes = collections.defaultdict(list)

    def add_link(self, link):
        """
        Add link to dictionary of links

        :param link: Link object
        """
        self.links[link.label] = link

    def add_connector(self, connector):
        """
        Add connector to dictionary of connectors

        :param connector: Connector object
        """

        self.connectors[connector.label] = connector

    def add_dispatcher(self, dispatcher):
        """
        Add dispatcher to dictionary of dispatchers

        :param dispatcher: Dispatcher object
        """

        self.dispatchers[dispatcher.road] = dispatcher

    def add_route(self, entry_road, route):
        """
        Add route to dictionary of routes

        :param entry_road: starting road
        :param route: list of road labels
        """
        self.routes[entry_road].append(route)

    def populate_scene(self):
        pass

    def clear(self):
        """
        Reinitialize Scene values
        """

        self.links.clear()
        self.connectors.clear()
        self.dispatchers.clear()
        self.entry_roads = []
        self.exit_roads = []
        self.routes.clear()

    def get_connector_by_conflict_group(self, group, conn):
        """
        Get the partner road of a connector using their conflict group

        :param group: conflict group
        :param conn: Connector object

        :return: Partner road (Connector object)
        """

        for connector in self.connectors.values():
            if conn != connector and group in connector.conflict_groups:
                return connector
