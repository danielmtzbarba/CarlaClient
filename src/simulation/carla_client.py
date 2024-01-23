import carla

from src.simulation.traffic_manager import TrafficManager
from src.simulation.hero import Hero 
from src.simulation.world import World
from src.simulation.scene import Scene

class CarlaClient(carla.Client):
    def __init__(self):
        super(CarlaClient, self).__init__('localhost', 2000)

        self.set_timeout(10.0)

        self.exit = False
        self.n_frame = 0
        self.vehicles = []
        self.vehicles_obj = []

        self.walkers = []
        self.controllers = []

        self.sensors = []
        self.sensors_obj = []

        self.world = World(self)
        self.world.setup(self.args)

        self.traffic = TrafficManager(self, self.args.traffic.tm_port)
        self.traffic.setup(self.args.traffic)
        self.scene = Scene(self.args)
        self.hero = Hero(self.args)
        self.hero.setup(self.world)
        actors, sensors = self.hero.spawn_sensors(self.world)
        self.sensors.extend(actors)
        self.sensors_obj.extend(sensors)
                
        for i in range(2):
            actor, vehicle = self.scene.spawn_vehicle(self.world, self.hero)
            self.vehicles.append(actor)
            self.vehicles_obj.append(vehicle)

        for i in range(2):
            actor, vehicle = self.scene.spawn_vehicle(self.world, self.hero)
            self.vehicles.append(actor)
            self.vehicles_obj.append(vehicle)

        if self.args.traffic.spawn_traffic:
            self.traffic.spawn_traffic()

# ----------------------------------------------------------------------
    def tick(self, timeout):

        if not self.args.hero.autopilot:
            self.hero.move()
            for car in self.vehicles_obj:
                car.move()

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
    def spawn_sync(self, batch):
        actor_id, success = None, False
        for response in self.apply_batch_sync(batch, True):
            if response.error:
                # Spawn failed on this location.
                pass
            else:
                actor_id = response.actor_id
                success = True
        return success, actor_id
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
        self.apply_batch([carla.command.DestroyActor(x.id) for x in actor_list])

    def destroy_actors(self):
        """
        Destroy all spawned actors during the simulation.
        """
        print('\nDestroying ego and %d sensors...' % len(self.sensors))
        self.destroy_batch([self.hero.actor])
        self.destroy_batch(self.sensors)

        print('Destroying %d walkers...' % len(self.walkers))
        self.destroy_batch(self.controllers)
        self.destroy_batch(self.walkers)

        print('Destroying %d vehicles...' % len(self.vehicles))
        self.destroy_batch(self.vehicles)

        print('\nDone.')

# ----------------------------------------------------------------------
