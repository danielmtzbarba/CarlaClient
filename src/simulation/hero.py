import os, random
import numpy as np
import carla

from src.simulation.route_planner import RoutePlanner
from carla import Transform, Location, Rotation

from src.sensors.camera import Camera
from src.sensors.lidar import Lidar

from src.simulation.vehicle import Vehicle

class Hero(Vehicle):
    def __init__(self, config):
        super(Hero, self).__init__(config)
        self.sensors = []
    
    def setup(self, world):
        """
        Sets a random start pose and spawns the ego.
        It also spawns and attachs the args.ego.sensors.
        """

        self._bp = world.get_bp(self._config.hero.bp)
        self._bp.set_attribute('role_name', 'hero')

        self._route_planner = RoutePlanner(world.map, self._config, speed=2)

        if self._config.hero.route:
            start_pose = self._route_planner.get_start_pose() 
        else:
            start_pose = random.choice(world.spawn_points)

        # Set carla autopilot
        if self._config.hero.autopilot:
            self.actor.set_autopilot(True, self._config.traffic.tm_port)

        self._current_w = world.map.get_waypoint(start_pose.location)
        self._actor = world.spawn_actor(self._bp, start_pose)    
        self._speed = self._config.hero.speed

    def spawn_sensors(self, world):
        # Spawn ego sensors
        actors, sensors = [], []

        for sensor_id in self._config.hero.sensors:
            
            sensor_config = getattr(self._config, sensor_id)
            savedir = os.path.join(self._config.logdir, sensor_config.id)
            actor, sensor = self.sensor_setup(world, sensor_config, savedir)

            actors.append(actor)
            sensors.append(sensor)

        return actors, sensors

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

