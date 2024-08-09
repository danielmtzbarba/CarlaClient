import carla
from random import randint
from carla import Transform, Location, Rotation
from src.simulation.vehicle import Vehicle
from src.simulation.pedestrian import Pedestrian


class Scene(object):
    def __init__(self, config):
        self._config = config

    def setup(self, world, hero):
        road_id, lane_id = hero.road, hero.lane
        v_actors, v_objs = [], []
        p_actors, p_objs = [], []

        for i in range(2):
            lane_id = (-(1**i)) * lane_id
            for i in range(self._config.n_vehicles):
                vehicle = self.try_vehicle_spawn(world, road_id, lane_id)
                if vehicle is not None:
                    v_actors.append(vehicle.actor)
                    v_objs.append(vehicle)

            for i in range(self._config.n_ped):
                pedestrian = self.try_pedestrian_spawn(world, road_id, lane_id)
                if pedestrian is not None:
                    p_actors.append(pedestrian.actor)
                    p_objs.append(pedestrian)

        return v_actors, v_objs, p_actors, p_objs

    def try_vehicle_spawn(self, world, road_id, lane_id):
        car = Vehicle(self._config.vehicle)
        spawned = False
        while not spawned:
            wp = None
            while wp == None:
                s = randint(self._config.min_s, self._config.max_s)
                wp = self.get_random_wp_in_road(world, road_id, lane_id, s)
            try:
                car.setup(world, wp)
                spawned = True
                return car
            except Exception as err:
                print(repr(err))

    def try_pedestrian_spawn(self, world, road_id, lane_id):
        pedestrian = Pedestrian(self._config.pedestrian)
        spawned = False
        while not spawned:
            wp = None
            while wp == None:
                s = randint(-200, 500)
                wp = self.get_random_wp_in_road(world, road_id, lane_id, s)
            loc = world.map.get_waypoint(
                wp.location, project_to_road=True, lane_type=(carla.LaneType.Sidewalk)
            ).transform.location
            loc = Location(loc.x, loc.y, loc.z + 1.0)
            angle = randint(0, 360)
            spwn_p = Transform(loc, Rotation(0, angle, 0))
            try:
                pedestrian.setup(world, spwn_p)
                spawned = True
                return pedestrian
            except Exception as err:
                print(repr(err))

    def get_random_wp_in_road(self, world, road_id, lane_id, s):
        wp = world.map.get_waypoint_xodr(road_id, lane_id, s)
        if wp:
            loc = wp.transform.location
            loc = Location(loc.x, loc.y, loc.z + 1.0)
            return Transform(loc, Rotation(0, 180, 0))
        return None
