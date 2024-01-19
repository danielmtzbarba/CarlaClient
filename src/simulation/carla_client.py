import carla

from src.simulation.traffic_manager import TrafficManager
from src.simulation.ego import Ego
from src.simulation.world import World

class CarlaClient(object):
    def __init__(self):
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)

        self.exit = False
        self.n_frame = 0
        self.vehicles = []
        self.walkers = []
        self.controllers = []
        self.sensors = []

        self.sensors_obj = []

        self.world = World(self.client)
        self.world.setup(self.args)

        self.traffic = TrafficManager(self.client, self.args.traffic.tm_port)
        self.traffic.setup(self.args.traffic)

        self.ego = Ego(self.world.get_bp(self.args.ego.bp))
        self.ego.setup(self.world, self.args)
        actors, sensors = self.ego.spawn_sensors(self.world, self.args)
        self.sensors.extend(actors)
        self.sensors_obj.extend(sensors)

        if self.args.traffic.spawn_traffic:
            self.traffic.spawn_traffic()

# ----------------------------------------------------------------------

    def sim_step(self):
        if not self.args.ego.autopilot:
            self.ego.move()

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
        self.client.apply_batch([carla.command.DestroyActor(self.ego.actor.id)])
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in self.sensors])

        print('Destroying %d walker_controllers...' % len(self.controllers))
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in self.controllers])

        print('Destroying %d walkers...' % len(self.walkers))
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in self.walkers])

        print('Destroying %d vehicles...' % len(self.vehicles))
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in self.vehicles])

        print('\nDone.')
    # ----------------------------------------------------------------------
