import carla

class Ego(object):
    def __init__(self, blueprint, config):
        self._ego_route, self._route_wps = [], []
        blueprint.set_attribute('role_name', 'hero')
    
    def setup(self, config):
        """
        Sets a random start pose and spawns the ego.
        It also spawns and attachs the args.ego.sensors.
        """
        if config.route:

            start_pose = self.ego_route_setup()
            self.ego = self.world.spawn_actor(ego_bp, start_pose)

        else:
            start_pose = random.choice(self.spawn_points)
            self.ego = self.world.spawn_actor(ego_bp, start_pose)
            self.current_w = self.map.get_waypoint(start_pose.location)
        
        # Spawn ego sensors
        for sensor in self.args.ego.sensors:
            sensor_args = getattr(self.args, sensor)
            self.sensor_setup(sensor_args)

        # Set carla autopilot
        if self.args.ego.autopilot:
            self.ego.set_autopilot(True, self.args.traffic.tm_port)
        
        self.traffic_manager.vehicle_percentage_speed_difference(self.ego,
                                                        self.args.ego.speed)
        
        self.traffic_manager.ignore_lights_percentage(self.ego, 100.0)
        
        print('\nSpawned 1 ego vehicle and %d sensors.' % len(self.sensors))

    def ego_route_setup(self):
        route_name = f'{self.args.ego.route}_{self.args.map}_seq_{self.args.seq}'
        route_path = os.path.join('src/routes/', f'{route_name}.npy')
        route = np.load(route_path)
        
        for i, p in enumerate(route):
            self._ego_route.append(carla.Location(p[0], p[1], p[2]))
        
        start_pose = carla.Transform(self._ego_route[0], carla.Rotation(0, 180, 0))
        self.current_w = self.map.get_waypoint(start_pose.location)

        return start_pose
    
    def ego_move(self, next_w):
        self.ego.set_transform(self.current_w.transform)
        self.current_w = next_w

    def ego_next_waypoint(self):
        """
        Ego vehicle follows predefined routes.
        Creates a new waypoint, and transforms the ego to that point.
        """
        if len(self._ego_route) > 0:
            if len(self._route_wps) < 1:
                next_route_loc = self._ego_route.pop(0)
                self._route_wps.extend(
                    route_planner(self.map, self.current_w.transform.location, 
                                  next_route_loc))
            next_w = self._route_wps.pop(0)

        else:
            if self.args.exit_after_route:
                self.exit = True
            next_w = random.choice(self.current_w.next(self.args.ego.speed))
        return next_w 
