from PySide2.QtCore import *
import weakref
import collections
from app.utils import const
import const as a_const


class AgentManager(QObject):

    agent_created = Signal()  # for observer class
    agent_moved = Signal()  # for observer class
    agent_deleted = Signal()  # for observer class

    def __init__(self, scene, clock):
        super(AgentManager, self).__init__(parent=None)
        self.agents = weakref.WeakKeyDictionary()
        self.scene = scene
        self.clock = clock
        self._road_index = collections.defaultdict(list)

    def add_agent(self, agent, road, pos, lane):
        self.agents[agent] = (road, pos, lane)
        self._road_index[road].append(agent)
        self.agent_created.emit()

    def remove_agent(self, agent):
        road, _, _ = self.agents[agent]
        self._road_index[road].remove(agent)
        del self.agents[agent]
        self.agent_deleted.emit()

    def move_agent(self, agent):
        road, pos, lane = self.agents[agent]

        new_acc = agent.deliberate_acc()
        new_vel = max(round(agent.vel + new_acc * (const.DT/100), 2), 0.0)
        new_pos = round(pos + new_vel * (const.DT/100), 2)

        if new_pos > road.length:
            try:
                new_road_label = agent.route.pop(0)  # get next road in agent's route
                new_road = self.scene.links[new_road_label] if new_road_label in self.scene.links \
                    else self.scene.connectors[new_road_label]

                self._road_index[road].remove(agent)
                self._road_index[new_road].append(agent)

            except IndexError:  # agent reached destination
                self.remove_agent(agent)
                new_road = None

            new_pos -= road.length
            dist_traveled = new_pos
        else:
            new_road = road

        new_lane = lane

        if new_road:
            agent.move(new_vel, new_acc, new_road, new_pos, new_lane)
            self.agents[agent] = (new_road, new_pos, new_lane)

    def update_agent_neighborhood(self, agent):
        agent.neighborhood = self.get_neighbors(agent)

    def update_agent_sight_distance(self, agent):
        agent.sight_distance = self.compute_ssd(agent.vel)

    def step(self):
        for agent in list(self.agents):
            self.update_agent_sight_distance(agent)
            self.update_agent_neighborhood(agent)
            self.move_agent(agent)

    def update_agent_time_active(self):
        for agent in self.agents:
            agent.time_active += 1

    @staticmethod
    def compute_ssd(velocity, grav=a_const.G, friction=a_const.F, perc_time=a_const.PRT, min_ssd=a_const.MIN_SIGHT_DIST):
        """
        Stopping sight distance (SSD) is a near worst-case distance a vehicle driver needs to be able to see in order
        have room to stop before colliding with an object ahead of the road.

        SSD is composed of the following:
        (1) Perception-Reaction Distance
             - the distance it takes for a road user to realize that a reaction is needed due to a road condition
             - equal to agent's velocity (in m/s) times the perception-reaction time (2.5 seconds)
        (2) Braking Distance
            - the distance it takes to complete the maneuver (braking)
            - equal to agent's velocity  (in m/s) divided by the product of twice the weight force acceleration
                due to gravity (19.6 m/s^2) and coefficient of friction between car tires and asphalt roads

        :param velocity: Velocity of sensing agent in m/s
        :param grav: Gravitational acceleration in m/s^2
        :param friction: Friction coefficient between car tires and road
        :param perc_time: Perception time in sec
        :param min_ssd: Minimum SSD in meters

        :return: SSD of the sensing agent in METERS. Minimum of 15.0 meters
        """
        braking_dist = velocity ** 2 / (grav * 2.0 * friction)
        perception_reaction_dist = velocity * perc_time
        ssd = braking_dist + perception_reaction_dist

        ssd = max(min_ssd, ssd)  # in m

        return ssd

    def get_neighbors(self, agent):
        my_road, my_pos, my_lane = self.agents[agent]
        ssd_front = agent.sight_distance

        neighborhood = dict(front=None, gap_front=a_const.LARGE_NUMBER)

        front_reach = my_pos + ssd_front

        # from same road
        section = self.members(my_road, start=my_pos,
                               end=front_reach if front_reach <= my_road.length else my_road.length)
        section.remove(agent)

        for _agent in section:
            _, pos, _ = self.agents[_agent]
            gap_front = round(pos - _agent.length - my_pos, 2)
            if neighborhood['front']:
                if pos < neighborhood['front'].position['pos']:
                    neighborhood['front'] = _agent
                    neighborhood['gap_front'] = gap_front
            else:
                neighborhood['front'] = _agent
                neighborhood['gap_front'] = gap_front

        # from different road
        if front_reach > my_road.length and agent.route:
            _road = self.scene.links[agent.route[0]] if agent.route[0] in self.scene.links \
                else self.scene.connectors[agent.route[0]]
            section = self.members(_road, start=0, end=min(front_reach - my_road.length, _road.length))

            for _agent in section:
                _, pos, _ = self.agents[_agent]
                gap_front = round(my_road.length + pos - _agent.length - my_pos, 2)
                if neighborhood['front']:
                    if pos < neighborhood['front'].position['pos'] and gap_front < neighborhood['gap_front']:
                        neighborhood['front'] = _agent
                        neighborhood['gap_front'] = gap_front
                else:
                    neighborhood['front'] = _agent
                    neighborhood['gap_front'] = gap_front

        return neighborhood

    def members(self, road, start=0, end=None, lane=None):
        members = list(self._road_index[road])

        if start or end is not None:
            end = road.length if end is None else end
            assert start <= end
            members = [agent for agent in members if self._filter_within(agent, road, start, end, lane)]
        return members

    def _filter_within(self, agent, road, start, end, lane):
        road_, pos, lane_ = self.agents[agent]

        if road_ == road:
            same_lane = True
            if lane is not None:
                same_lane = lane == lane_
            rear = pos - agent.length
            return ((start <= pos <= end or start <= rear <= end) or (rear <= start <= pos and rear <= end <= pos))\
                and same_lane
        return False

    def reset(self):
        for agent in list(self.agents):
            self.remove_agent(agent)
