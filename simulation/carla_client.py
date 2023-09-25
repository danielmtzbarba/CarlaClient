import os
import random
import carla
from carla import Transform, Location, Rotation

from simulation.sensors.camera import Camera

map_layers = {
    'Vegetation':  carla.CityObjectLabel.Vegetation,
    'Buildings': carla.CityObjectLabel.Buildings,
    'Bridge': carla.CityObjectLabel.Bridge,
    'Walls': carla.CityObjectLabel.Walls,
    'Fences': carla.CityObjectLabel.Fences,

    'TraffiSigns': carla.CityObjectLabel.TrafficSigns,
    'Poles': carla.CityObjectLabel.Poles,
    'RoadLines': carla.CityObjectLabel.RoadLines,
    'GuardRail': carla.CityObjectLabel.GuardRail,
    'RailTrack': carla.CityObjectLabel.RailTrack,
    'Static': carla.CityObjectLabel.Static,
    'Dynamic': carla.CityObjectLabel.Dynamic, 
    'Other': carla.CityObjectLabel.Other,
}

class CarlaClient(object):
    actor_list = []
    sensors = []

    def __init__(self):
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(5.0)

        self.traffic_manager = self.client.get_trafficmanager(8000)
        self.world_setup()
        self.ego_setup()

    def world_setup(self):
        """
        Applies the args.world_args to the carla.WorldSettings.
        It also gets map, bp_library and spawn_points.
        Toggles off the defined map layers.
        """
        self.world = self.client.get_world()
        self.og_settings = self.get_world_settings()
        self.bp_library = self.world.get_blueprint_library()
        self.map = self.world.get_map()
        self.spawn_points = self.get_spawn_points()
        self.toogle_map_layers(on=False)
    
    def sensor_setup(self, sensor_args):
        actor = self.spawn_actor(sensor_args, self.ego)
        if 'camera' in sensor_args.bp:
            sensor = Camera(actor, sensor_args)

        sensor.save_path = os.path.join(self.args.output_path,
                                        self.args.map,
                                        self.args.test_id)
        self.sensors.append(sensor)

    def ego_setup(self):
        """
        Sets a random start pose and spawns the ego.
        It also spawns and attachs the args.ego.sensors.
        """
        # Spawn ego vehicle
        self._start_pose = random.choice(self.spawn_points)
        self._waypoint = self.map.get_waypoint(self._start_pose.location)

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
        self._waypoint = random.choice(self._waypoint.next(0.5))
        self.ego.set_transform(self._waypoint.transform)

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

    def toogle_map_layers(self, on=False):
        """
        Toggle off objects from specific environment layers.
        """
        for layer in self.args.remove_layers:      
            layer_objs = self.world.get_environment_objects(map_layers[layer])
            objects_to_toggle = {x.id for x in layer_objs}
            self.world.enable_environment_objects(objects_to_toggle, on)
    
    def destroy_actors(self):
        """
        Destroy all spawned actors during the simulation.
        """
        for actor in self.actor_list:
            actor.destroy()