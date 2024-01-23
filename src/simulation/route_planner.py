import os
import numpy as np
import carla

from src.agents.navigation.global_route_planner import GlobalRoutePlanner
from carla import Transform, Location, Rotation

class RoutePlanner(object):
    def __init__(self, map, config, speed):
        self._map = map
        self._config = config
        self._speed = speed
        self._route, self._wps = [], []

    def get_start_pose(self):
        route_name = f'{self._config.hero.route}_{self._config.map}_seq_{self._config.seq}'
        route_path = os.path.join('src/routes/', f'{route_name}.npy')
        route = np.load(route_path)

        for p in route:
            self._route.append(Location(p[0], p[1], p[2]))

        return Transform(self._route[0], Rotation(0, self._config.hero.spawn_angle , 0))

    def get_waypoints(self, a, b):
        grp = GlobalRoutePlanner(self._map, self._speed)
        waypoints = grp.trace_route(a, b)
        return [w[0] for w in waypoints]

    def next_waypoint(self, current_w):
        """
        Ego vehicle follows predefined routes.
        Creates a new waypoint, and transforms the ego to that point.
        """
        if len(self._route) > 0:
            if len(self._wps) < 1:
                next_route_loc = self._route.pop(0)
                self._wps.extend(
                self.get_waypoints(current_w.transform.location, 
                              next_route_loc))
            next_w = self._wps.pop(0)

        else:
            if self.args.exit_after_route:
                self.exit = True
            next_w = random.choice(current_w.next(self.args.ego.speed))
        return next_w 

    def draw_route(self, world, waypoints):
        i = 0
        for w in waypoints:
            if i % 10 == 0:
                world.debug.draw_string(w.transform.location, 'o', draw_shadow=False,
                color=carla.Color(r=255, g=0, b=0), life_time=5.0,
                persistent_lines=False)
            else:
                world.debug.draw_string(w.transform.location, 'o', draw_shadow=False,
                color = carla.Color(r=0, g=0, b=255), life_time=5.0,
                persistent_lines=False)
            i += 1
        return None

    @property
    def lenght_route(self):
        return len(self._route)
