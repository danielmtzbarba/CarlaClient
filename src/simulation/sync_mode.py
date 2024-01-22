#!/usr/bin/env python

import carla
import queue

from src.simulation.carla_client import CarlaClient

class CarlaSyncMode(CarlaClient):
    """
    Context manager to synchronize output from different sensors. Synchronous
    mode is enabled as long as we are inside this context

        with CarlaSyncMode(world, sensors) as sync_mode:
            while True:
                data = sync_mode.tick(timeout=1.0)

    """

    def __init__(self, args, **kwargs):
        self.args = args
        super().__init__()
        self.frame = None
        self.delta = 1.0 / kwargs.get('fps', 20)
        self._queues = []

    def __enter__(self):

        self.world.sync_mode(self.delta)
        def make_queue(register_event):
            q = queue.Queue()
            register_event(q.put)
            self._queues.append(q)

        make_queue(self.world.get_world().on_tick)

        # Sensor queues to retreieve data
        for actor in self.sensors:
            make_queue(actor.listen)
        return self

    def __exit__(self, *args, **kwargs):
        self.stop_sensors()
        self.stop_controllers()
        self.destroy_actors()
        self.world.reset_settings()
