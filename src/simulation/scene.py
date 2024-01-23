import carla
from random import randint
from carla import Transform, Location, Rotation
from src.simulation.vehicle import Vehicle

class Scene(object):
    def __init__(self, config):
        self._config = config

    def setup(self):
        pass

    def random_spawn_in_lane(self, world, vehicle):
        road, lane = vehicle.road, vehicle.lane
        s = randint(50, 100)
        wp = world.map.get_waypoint_xodr(road,lane, s)
        if wp == None:
            wp = world.map.get_waypoint(vehicle.location,project_to_road=True, lane_type=(carla.LaneType.Driving))
        loc = wp.transform.location
        loc = Location(loc.x, loc.y, 0.3)
        return Transform(loc, Rotation(0, 180, 0))

    def spawn_vehicle(self, world, vehicle):
        spwn_p = self.random_spawn_in_lane(world, vehicle)
        car = Vehicle(self._config)
        return car.setup(world, spwn_p)     
