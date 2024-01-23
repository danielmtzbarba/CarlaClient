import os, random
import numpy as np
import carla

from src.simulation.route_planner import RoutePlanner
from carla import Transform, Location, Rotation

class Vehicle(object):
    def __init__(self, config):
        self._config = config
        self.current_w = None
    
    def setup(self, world, start_pose=None):
        """
        Sets a random start pose and spawns the ego.
        It also spawns and attachs the args.ego.sensors.
        """
        self._bp = world.get_random_vehicle_bp()
        self._route_planner = RoutePlanner(world.map,
                                        self._config, speed=2)


        if self._config.vehicle.route:
            start_pose = self._route_planner.get_start_pose() 

        else:
            if start_pose is None:
                start_pose = random.choice(world.spawn_points)


        self._actor = world.spawn_actor(self._bp, start_pose)    
        self._current_w = world.map.get_waypoint(start_pose.location)

        # Set carla autopilot
        if self._config.vehicle.autopilot:
            self._actor.set_autopilot(True, self._config.traffic.tm_port)
        return self._actor, self

    def move(self):
        self._actor.set_transform(self._current_w.transform)

        if self._route_planner.lenght_route > 0:
            self._current_w = self._route_planner.next_waypoint(self._current_w) 
        else:
            self._current_w = random.choice(self._current_w.next(self._config.vehicle.speed))

    @property   
    def location(self):
        return self._actor.get_location()

    @property
    def current_wp(self):
        return self._current_w

    @property   
    def road(self):
        return self._current_w.road_id

    @property   
    def lane(self):
        return self._current_w.lane_id

    @property
    def bp(self):
        return self._bp

    @property
    def actor(self):
        return self._actor
