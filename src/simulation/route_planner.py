from src.agents.navigation.global_route_planner import GlobalRoutePlanner

class RoutePlanner(object):
    def __init__(self, map, resolution):
        self._map = map
        self._resolution = resolution

    def get_waypoints(self, a, b):
        grp = GlobalRoutePlanner(self._map, self._resolution)
        waypoints = grp.trace_route(a, b)
        return [w[0] for w in waypoints]
