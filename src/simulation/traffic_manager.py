import src.simulation.traffic as traffic

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
    

    def spawn_traffic(self, world, config):

        # Spawn vehicles
        vehicles_list = traffic.spawn_vehicles(config, self.client,
                                        self.bp_library, self.spawn_points)
        
        self.vehicles.extend(self.world.get_actors(vehicles_list))
        print('Spawned %d vehicles.' % (len(self.vehicles)))

        # Spawn Walkers
        (self.walkers,
         walkers_speed,
         self.controllers) = traffic.spawn_walkers(self.args.traffic, self.client, 
                                               self.world, self.bp_library)
        
        # Initialize walkers controllers and set target to walk 
        for walker_controller, speed in zip(self.controllers, walkers_speed):
            # start walker
            walker_controller.start()
            # set walk to random point
            walker_controller.go_to_location(self.world.get_random_location_from_navigation())
            # max speed
            walker_controller.set_max_speed(float(speed))

        print('Spawned %d walkers and %d controllers, press Ctrl+C to exit.'
               % (len(self.walkers), len(self.controllers)))
    
    def change_traffic_light_timings(self, world):
        list_actor = world.get_actors()
        for actor_ in list_actor:
            if isinstance(actor_, carla.TrafficLight):
                 # for any light, first set the light state, then set time. for yellow it is 
                 # carla.TrafficLightState.Yellow and Red it is carla.TrafficLightState.Red
                actor_.set_state(carla.TrafficLightState.Green) 
                actor_.set_green_time(10000.0)

    def percentage_speed_diff(self, vehicle , speed): 
        self.manager.vehicle_percentage_speed_difference(vehicle,
                                                        speed)

    def ignore_traffic_lights(self, vehicle, percentage):
        self.manager.ignore_lights_percentage(vehicle, percentage)

    def get_manager(self):
        return self.manager
