from PySide2.QtCore import *
import ZODB
import transaction


class ConflictManager(QObject):

    def __init__(self, clock, scene, agent_manager):
        super(ConflictManager, self).__init__(parent=None)
        self.clock = clock
        self.scene = scene
        # self.conflict_zones = scene.conflict_zones
        self.agent_manager = agent_manager

        self.agent_manager.agent_created.connect(self._new_agent_callback)
        # self.clock.fine.connect(self._clock_signal_callback)

    def _new_agent_callback(self, params):
        if 'agent' in params:
            params['agent'].intention_enter.connect(self._agent_intention_enter_callback)
            params['agent'].intention_exit.connect(self._agent_intention_exit_callback)

    # def _clock_signal_callback(self):
    #     for value in self.conflict_zones.values():
    #         if value:
    #             zone = value[0]
    #
    #             if not self.agent_manager.members(zone.road):
    #                 zone.locked = False

    def _agent_intention_enter_callback(self, params):
        road = params['road']
        gap = params['gap']
        conflict_groups = road.conflict_groups

        for group in conflict_groups:
            partner_road = self.scene.get_connector_by_conflict_group(group, road)
            if not self.agent_manager.members(partner_road) and not road.locked:
                partner_road.locked = True
                transaction.commit()

    def _agent_intention_exit_callback(self, params):
        road = params['road']
        conflict_groups = road.conflict_groups

        for group in conflict_groups:
            partner_road = self.scene.get_connector_by_conflict_group(group, road)
            partner_road.locked = False
            transaction.commit()
