from PySide2.QtCore import *
import ZODB
import transaction


class ConflictManager(QObject):
    """
    Handles conflict resolution
    """

    def __init__(self, clock, scene, agent_manager):
        """
        Initialize conflict manager

        :param clock: simulation clock (Clock object)
        :param scene: Scene object
        :param agent_manager: AgentManager object
        """

        super(ConflictManager, self).__init__(parent=None)
        self.clock = clock
        self.scene = scene
        self.agent_manager = agent_manager

        self.agent_manager.agent_created.connect(self._new_agent_callback)

    def _new_agent_callback(self, params):
        """
        Responds to 'agent_created' signal emitted by AgentManager

        :param params: dictionary containing parameters
        """

        if 'agent' in params:
            params['agent'].intention_enter.connect(self._agent_intention_enter_callback)
            params['agent'].intention_exit.connect(self._agent_intention_exit_callback)

    def _agent_intention_enter_callback(self, params):
        """
        Responds to 'intention_enter' signal emitted by Agent
        Handles locking of connectors when an agent intends to enter a conflict area/intersection

        :param params: dictionary containing parameters
        """

        road = params['road']
        gap = params['gap']
        conflict_groups = road.conflict_groups

        for group in conflict_groups:
            partner_road = self.scene.get_connector_by_conflict_group(group, road)
            if partner_road:
                if not self.agent_manager.members(partner_road) and road.locked:
                    road.locked = False
                    partner_road.locked = True
                elif not self.agent_manager.members(partner_road) and not road.locked:
                    road.locked = False
                    partner_road.locked = True
                elif self.agent_manager.members(partner_road):
                    road.locked = True
                    partner_road.locked = False
                transaction.commit()

    def _agent_intention_exit_callback(self, params):
        """
        Responds to 'intention_exit' signal emitted by Agent
        Handles unlocking of connectors when an agent intends to exit a conflict area/intersection

        :param params:
        """
        road = params['road']
        conflict_groups = road.conflict_groups

        for group in conflict_groups:
            partner_road = self.scene.get_connector_by_conflict_group(group, road)
            if partner_road:
                partner_road.locked = False
                transaction.commit()
