import os, random
import numpy as np
import carla

from src.simulation.route_planner import RoutePlanner
from carla import Transform, Location, Rotation

from src.sensors.camera import Camera
from src.sensors.lidar import Lidar

class Ego(object):
    def __init__(self, blueprint):
        self.sensors = []
        self._route, self._wps = [], []
        self.current_w = None
        self._bp = blueprint 
        self._bp.set_attribute('role_name', 'hero')
    
    def setup(self, world, config):
        """
        Sets a random start pose and spawns the ego.
        It also spawns and attachs the args.ego.sensors.
        """

        self._route_planner = RoutePlanner(world.map, resolution=2)

        if config.ego.route:
            route_name = f'{config.ego.route}_{config.map}_seq_{config.seq}'
            route_path = os.path.join('src/routes/', f'{route_name}.npy')
            route = np.load(route_path)
            
            for p in route:
                self._route.append(Location(p[0], p[1], p[2]))
            
            start_pose = Transform(self._route[0], Rotation(0, 180, 0))

        else:
            start_pose = random.choice(world.spawn_points)

        # Set carla autopilot
        if config.ego.autopilot:
            self.actor.set_autopilot(True, config.traffic.tm_port)

        self._current_w = world.map.get_waypoint(start_pose.location)
        self._actor = world.spawn_actor(self._bp, start_pose)    
    
    def spawn_sensors(self, world, config):
        # Spawn ego sensors
        actors, sensors = [], []

        for sensor_id in config.ego.sensors:
            
            sensor_config = getattr(config, sensor_id)
            savedir = os.path.join(config.logdir, sensor_config.id)
            actor, sensor = self.sensor_setup(world, sensor_config, savedir)

            actors.append(actor)
            sensors.append(sensor)

        return actors, sensors

        ''' 
        
        #self.traffic_manager.vehicle_percentage_speed_difference(self.ego,
        #                                                self.args.ego.speed)
        
        #self.traffic_manager.ignore_lights_percentage(self.ego, 100.0)
        
        print('\nSpawned 1 ego vehicle and %d sensors.' % len(self.sensors))
        ''' 
   
    def sensor_setup(self, world, config, savedir):
        bp = world.get_bp(config.bp)

        for key, val in config.params.items():
            bp.set_attribute(key, str(val))
        
        transform = Transform(Location(*config.location),
                               Rotation(*config.rotation))
        
        actor = world.spawn_actor(bp, transform, self.actor)
        if 'camera' in config.bp:
            sensor = Camera(actor, config)
        if 'lidar' in config.bp:
            sensor = Lidar(actor, config)

        sensor.save_path = savedir 
        
        if config.id == 'bev':
            sensor.save_path = os.path.join(sensor.save_path, "sem")

        return actor, sensor

    def move(self):
        self._actor.set_transform(self._current_w.transform)
        self._current_w = self.next_waypoint() 

    def next_waypoint(self):
        """
        Ego vehicle follows predefined routes.
        Creates a new waypoint, and transforms the ego to that point.
        """
        if len(self._route) > 0:
            if len(self._wps) < 1:
                next_route_loc = self._route.pop(0)
                self._wps.extend(
                self._route_planner.get_waypoints(self._current_w.transform.location, 
                              next_route_loc))
            next_w = self._wps.pop(0)

        else:
            if self.args.exit_after_route:
                self.exit = True
            next_w = random.choice(self._current_w.next(self.args.ego.speed))
        return next_w 
    
    @property
    def bp(self):
        return self._bp

    @property
    def actor(self):
        return self._actor
