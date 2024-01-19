import carla

class World(object)
    def __init__(self, client):
        self._world = client.get_world()

    def setup(self, config):
        """
        Applies the args.world_args to the carla.WorldSettings.
        It also gets map, bp_library and spawn_points.
        """
        self.og_settings = self._world.get_settings()

        self.map = self._world.get_map()
        self.debug = self._world.debug

        self.bp_library = self._world.get_blueprint_library()
        self.spawn_points = self.map.get_spawn_points()

        self._world.set_pedestrians_seed(config.seed)
        self._world.set_pedestrians_cross_factor(config.traffic.percent_crossing)

    def get_bp(self, id):
        return self.bp_library.find(id)
    
    def spawn_actor(self, bp, transform, attached=None):
        if attached:
            return self.world.spawn_actor(bp, transform, attach_to=vehicle)
        return self.world.spawn_actor(bp, transform)

