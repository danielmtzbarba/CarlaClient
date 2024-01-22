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
    def tick(self, timeout):

        if not self.args.ego.autopilot:
            self.ego.move()

        self.frame = self.world.get_world().tick()
        self.n_frame += 1

        data = [self._retrieve_data(q, timeout) for q in self._queues]

        for sensor, frame in zip(self.sensors_obj, data[1:]):
            sensor.set_frame(frame)

        assert all(x.frame == self.frame for x in data)
        return data
    
    def _retrieve_data(self, sensor_queue, timeout):
        while True:
            data = sensor_queue.get(timeout=timeout)
            if data.frame == self.frame:
                return data

# ----------------------------------------------------------------------

    def stop_sensors(self):
        for actor in self.sensors:
            if actor.is_listening():
                actor.stop()

        for q in self._queues:
            with q.mutex:
                q.queue.clear()

    def stop_controllers(self):
        # Stop controllers 
        for walker_controller in self.controllers:
            walker_controller.stop()

# ----------------------------------------------------------------------

    def destroy_batch(self, actor_list): 
        self.client.apply_batch([carla.command.DestroyActor(x.id) for x in actor_list])

    def destroy_actors(self):
        """
        Destroy all spawned actors during the simulation.
        """
        print('\nDestroying ego and %d sensors...' % len(self.sensors))
        self.destroy_batch([self.ego.actor])
        self.destroy_batch(self.sensors)

        print('Destroying %d walkers...' % len(self.walkers))
        self.destroy_batch(self.controllers)
        self.destroy_batch(self.walkers)

        print('Destroying %d vehicles...' % len(self.vehicles))
        self.destroy_batch(self.vehicles)

        print('\nDone.')

# ----------------------------------------------------------------------
