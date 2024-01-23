import carla
import random

class World(object):
    def __init__(self, client):
        self._world = client.get_world()
        self._map = self._world.get_map()
        self._debug = self._world.debug

    def setup(self, config):
        """
        Applies the args.world_args to the carla.WorldSettings.
        It also gets map, bp_library and spawn_points.
        """
        self._og_settings = self._world.get_settings()

        self._bp_library = self._world.get_blueprint_library()
        self._vehicle_bps = self._bp_library.filter("vehicle.*")
        self._spawn_points = self._map.get_spawn_points()

        self._world.set_pedestrians_seed(config.seed)
        self._world.set_pedestrians_cross_factor(config.traffic.percent_crossing)

    
    def sync_mode(self, delta):
        self._world.apply_settings(
            carla.WorldSettings(
            no_rendering_mode=False,
            synchronous_mode=True,
            fixed_delta_seconds=delta))
    
    def reset_settings(self):
        self._world.apply_settings(self._og_settings)

    def get_random_vehicle_bp(self):
        return random.choice(self._vehicle_bps)

    def get_bp(self, id):
        return self._bp_library.find(id)
    
    def spawn_actor(self, bp, transform, attached=False):
        if attached:
            return self._world.spawn_actor(bp, transform, attach_to=attached)
        return self._world.spawn_actor(bp, transform)
    
    def get_waypoint(self, location):
        return self._map.get_waypoint(location)
    
    def get_world(self):
        return self._world

    @property
    def spawn_points(self):
        return self._spawn_points

    @property
    def map(self):
        return self._map

