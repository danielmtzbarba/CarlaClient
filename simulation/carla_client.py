import os
import random
import carla
from carla import Transform, Location, Rotation

from simulation.sensors.camera import Camera
from simulation.sensors.lidar import Lidar

class CarlaClient(object):
    def __init__(self):
        self.actor_list = []
        self.sensors = []
        self.n_frame = 0
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(5.0)

        self.traffic_manager = self.client.get_trafficmanager(8000)
        self.world_setup()
        self.ego_setup()
    
    def world_setup(self):
        """
        Applies the args.world_args to the carla.WorldSettings.
        It also gets map, bp_library and spawn_points.
        """
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        self.debug = self.world.debug

        self.og_settings = self.get_world_settings()
        self.bp_library = self.world.get_blueprint_library()
        self.spawn_points = self.get_spawn_points()
    
    def sensor_setup(self, sensor_args):
        actor = self.spawn_actor(sensor_args, self.ego)
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
        
        self.sensors.append(sensor)

    def ego_setup(self):
        """
        Sets a random start pose and spawns the ego.
        It also spawns and attachs the args.ego.sensors.
        """
        # Spawn ego vehicle
        self._start_pose = random.choice(self.spawn_points)
        self.current_w = self.map.get_waypoint(self._start_pose.location)

        self.ego = self.world.spawn_actor(self.bp_library.filter(self.args.ego.bp)[0],
                                          self._start_pose)
        self.actor_list.append(self.ego)

        # Spawn ego sensors
        for sensor_args in self.args.ego.sensors:
            self.sensor_setup(sensor_args)

        # Set carla autopilot
        if self.args.ego.autopilot:
            tm_port = self.traffic_manager.get_port()
            self.ego.set_autopilot(True, tm_port)
    
    def ego_next_waypoint(self):
        """
        Ego vehicle follows predefined routes.
        Creates a new waypoint, and transforms the ego to that point.
        """
        self.next_w = random.choice(
            self.current_w.next(self.args.ego.speed))
        
        self.ego.set_transform(self.current_w.transform)
        self.current_w = self.next_w

    def get_world_settings(self):
        """
        Wrapper of the WorldSettings getter function.

        Returns:
            Carla.WorldSettings: Object containing WorldSettings.
        """
        return self.world.get_settings()
    
    def apply_world_settings(self, settings):
        """
        Wrapper of the carla.WorldSettings setters function.
        """
        self.world.apply_settings(settings)
    
    def get_spawn_points(self):
        """
        Wrapper of the spawn points getter function.

        Returns:
            List: Contains map's spawn points.
        """
        return self.map.get_spawn_points()
    
    def spawn_actor(self, actor_args, attach_to=None):
        """
        Spawn an actor in the specified coordinates.
        
        Args:
            actor_args (obj):  Object with attributes the following attributes:

                bp: String of the blueprint's base_type. 
                params: Additional parameters for the actor blueprints 
                transform: Actor's spawn coordinates (location and rotation).
            
            attach_to: (carla.Actor): Useful for sensors. Attach to another actor. 
                
        Returns:
            carla.Actor
        """
        bp = self.bp_library.find(actor_args.bp)
        for key, val in vars(actor_args.params).items():
            bp.set_attribute(key, val)
            
        transform = Transform(Location(*actor_args.location),
                               Rotation(*actor_args.rotation))
        # Spawn sensors.
        if attach_to:
            actor = self.world.spawn_actor(bp, transform, attach_to=attach_to)

        # Spawn other actors (Vehicles, etc.)
        else:
            actor = self.world.spawn_actor(bp, transform)

        self.actor_list.append(actor)
        return actor

    def destroy_actors(self):
        """
        Destroy all spawned actors during the simulation.
        """
        for actor in self.actor_list:
            actor.destroy()