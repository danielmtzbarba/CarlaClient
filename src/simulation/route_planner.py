import os
import random
import numpy as np
import carla

from src.agents.navigation.global_route_planner import GlobalRoutePlanner
from carla import Transform, Location, Rotation

def are_same_point(point, point_list, tsh):

    point = np.array((point.x, point.y))
    for p in point_list:
        p = np.array((p.x, p.y))
        dist = np.linalg.norm(point - p)
        if dist < tsh:
            return True
    return False

def plot_points(world, point, id ,color=carla.Color(r=255, g=255, b=0)):
    world.debug.draw_string(point, str(id), draw_shadow=False,
                            color=color, life_time=10.0,
                            persistent_lines=False)

class RoutePlanner(object):
    def __init__(self, world, config, speed):
        self._world = world
        try:
            self._map = world.map
        except:
            self._map = world.get_map()
        self._config = config
        self._speed = speed
        self._route, self._wps = [], []
        self._get_road_wps()

    def get_start_pose(self):
        self.create_route(self._config.scene.route)
        spawn_loc = self._route.pop(0)
        spawn_loc.z = 2 
        return Transform(spawn_loc,
                           Rotation(0, self._config.hero.spawn_angle, 0))
      
    def _get_road_wps(self):
        self._roads = self._map.get_topology()
        self._road_ids, self._road_wps = [], []

        i = 0
        for road in self._roads:
            point = road[0]
            id = point.id
            point = point.transform.location

            if not are_same_point(point, self._road_wps, 2):
                plot_points(self._world, point, i)
                self._road_wps.append(point)
                self._road_ids.append(id)
                i += 1
    
    def create_route(self, route):
       for wp_id in route:
            road_wp  = self.road_wps[wp_id]
            self._route.append(road_wp)
        
    def get_route_waypoints(self, a, b):
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
                self.get_route_waypoints(current_w.transform.location, 
                              next_route_loc))
#                self.draw_route(self._wps)
            next_w = self._wps.pop(0)

        else:
            if self._config.exit_after_route:
                self.exit = True
            next_w = random.choice(current_w.next(self._config.speed))
        return next_w 

    def draw_route(self, waypoints):
        i = 0
        for w in waypoints:
            if i % 10 == 0:
                self._world.debug.draw_string(w.transform.location, 'o', draw_shadow=False,
                color=carla.Color(r=255, g=0, b=0), life_time=5.0,
                persistent_lines=False)
            else:
                self._world.debug.draw_string(w.transform.location, 'o', draw_shadow=False,
                color = carla.Color(r=0, g=0, b=255), life_time=5.0,
                persistent_lines=False)
            i += 1
        return None

    @property
    def route(self):
        return self._wps

    @property
    def road_wps(self):
        return self._road_wps 

    @property
    def lenght_route(self):
        return len(self._route)
