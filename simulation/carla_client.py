import os, time, random

import carla
from carla import Transform, Location, Rotation

from simulation.sensors.camera import Camera
from simulation.sensors.lidar import Lidar

from simulation.generate_traffic import spawn_vehicles, spawn_walkers

class CarlaClient(object):
    def __init__(self):
        self.n_frame = 0
        self.vehicles = []
        self.walkers = []
        self.controllers = []
        self.sensors = []

        self.sensors_obj = []

   
        if self.args.seed is None:
            self.args.seed = 42

        random.seed(self.args.seed)

        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(5.0)

        self.world_setup()
        self.traffic_setup()
        self.ego_setup()
        self.spawn_traffic()

    def world_setup(self):
        """
        Applies the args.world_args to the carla.WorldSettings.
        It also gets map, bp_library and spawn_points.
        """
        self.world = self.client.get_world()
        self.og_settings = self.world.get_settings()

        self.map = self.world.get_map()
        self.debug = self.world.debug

        self.bp_library = self.world.get_blueprint_library()
        self.spawn_points = self.map.get_spawn_points()

        self.world.set_pedestrians_seed(self.args.seed)

    def traffic_setup(self):
        self.traffic_manager = self.client.get_trafficmanager(self.args.traffic.tm_port)
        self.traffic_manager.set_global_distance_to_leading_vehicle(2.5)

        if self.args.traffic.tm_hybrid:
            self.traffic_manager.set_hybrid_physics_mode(True)
            self.traffic_manager.set_hybrid_physics_radius(70.0)
        
        self.traffic_manager.set_random_device_seed(self.args.seed)
        self.traffic_manager.set_synchronous_mode(True)

        self.traffic_manager.global_percentage_speed_difference(self.args.traffic.vehicle_speed)
        self.world.set_pedestrians_cross_factor(self.args.traffic.percent_crossing)
    
    # ----------------------------------------------------------------------  
    def sensor_setup(self, sensor_args):
        bp = self.bp_library.find(sensor_args.bp)

        for key, val in vars(sensor_args.params).items():
            bp.set_attribute(key, val)
            
        transform = Transform(Location(*sensor_args.location),
                               Rotation(*sensor_args.rotation))
        
        actor = self.world.spawn_actor(bp, transform, attach_to=self.ego)
        if 'camera' in sensor_args.bp:
            sensor = Camera(actor, sensor_args)
        if 'lidar' in sensor_args.bp:
            sensor = Lidar(actor, sensor_args)

        sensor.save_path = os.path.join(self.args.output_path,
                                        self.args.map,
                                        self.args.test_id,
                                        sensor_args.id)
        
        if sensor_args.id == 'bev':
            sensor.save_path = os.path.join(sensor.save_path, "sem")
        self.sensors.append(actor)
        self.sensors_obj.append(sensor)

    def ego_setup(self):
        """
        Sets a random start pose and spawns the ego.
        It also spawns and attachs the args.ego.sensors.
        """
        # Spawn ego vehicle
        self._start_pose = random.choice(self.spawn_points)
        self.current_w = self.map.get_waypoint(self._start_pose.location)
        
        ego_bp = self.bp_library.filter(self.args.ego.bp)[0]
        ego_bp.set_attribute('role_name', 'hero')

        self.ego = self.world.spawn_actor(ego_bp, self._start_pose)

        # Spawn ego sensors
        for sensor_args in self.args.ego.sensors:
            self.sensor_setup(sensor_args)

        # Set carla autopilot
        if self.args.ego.autopilot:
            self.ego.set_autopilot(True, self.args.traffic.tm_port)
        
        self.traffic_manager.vehicle_percentage_speed_difference(self.ego,
                                                        self.args.ego.speed)
        
        self.traffic_manager.ignore_lights_percentage(self.ego, 100.0)
        
        print('\nSpawned 1 ego vehicle and %d sensors.' % len(self.sensors))

    
    def ego_next_waypoint(self):
        """
        Ego vehicle follows predefined routes.
        Creates a new waypoint, and transforms the ego to that point.
        """
        self.next_w = random.choice(
            self.current_w.next(self.args.ego.speed))
        
        self.ego.set_transform(self.current_w.transform)
        self.current_w = self.next_w

# ----------------------------------------------------------------------
    def spawn_traffic(self):

        # Spawn vehicles
        vehicles_list = spawn_vehicles(self.args.traffic, self.client,
                                        self.bp_library, self.spawn_points)
        
        self.vehicles.extend(self.world.get_actors(vehicles_list))
        print('Spawned %d vehicles.' % (len(self.vehicles) - 1))

        # Spawn Walkers
        (self.walkers,
         walkers_speed,
         self.controllers) = spawn_walkers(self.args.traffic, self.client, 
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
        
    # ----------------------------------------------------------------------
    def stop_controllers(self):
        # Stop controllers 
        for walker_controller in self.controllers:
            walker_controller.stop()

    def destroy_actors(self):
        """
        Destroy all spawned actors during the simulation.
        """
        print('\nDestroying ego and %d sensors...' % len(self.sensors))
        self.client.apply_batch([carla.command.DestroyActor(self.ego.id)])
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in self.sensors])

        print('Destroying %d walker_controllers...' % len(self.controllers))
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in self.controllers])

        print('Destroying %d walkers...' % len(self.walkers))
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in self.walkers])

        print('Destroying %d vehicles...' % len(self.vehicles))
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in self.vehicles])

        print('\nDone.')