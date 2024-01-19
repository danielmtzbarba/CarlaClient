class TrafficManager(object):
    def __init__(self, client, port):
        self.manager = client.get_trafficmanager(port)

    def setup(self, config):
        self.manager.set_global_distance_to_leading_vehicle(2.5)

        if config.tm_hybrid:
            self.manager.set_hybrid_physics_mode(True)
            self.manager.set_hybrid_physics_radius(70.0)
        
        self.manager.set_random_device_seed(config.seed)
        self.manager.set_synchronous_mode(True)
    
    def get_manager(self):
        return self.manager
