#!/usr/bin/env python

import carla
import queue

from simulation.carla_client import CarlaClient

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
        self.delta_seconds = 1.0 / kwargs.get('fps', 20)
        self._queues = []

    def __enter__(self):
        self.frame = self.apply_world_settings(carla.WorldSettings(
            no_rendering_mode=False,
            synchronous_mode=True,
            fixed_delta_seconds=self.delta_seconds))

        def make_queue(register_event):
            q = queue.Queue()
            register_event(q.put)
            self._queues.append(q)

        make_queue(self.world.on_tick)

        # Sensor queues to retreieve data
        for sensor in self.sensors:
            actor = sensor.get_actor()
            make_queue(actor.listen)
        return self

    def tick(self, timeout):
        self.frame = self.world.tick()
        self.n_frame += 1
        data = [self._retrieve_data(q, timeout) for q in self._queues]

        for sensor, frame in zip(self.sensors, data[1:]):
            sensor.set_frame(frame)

        assert all(x.frame == self.frame for x in data)
        return data

    def __exit__(self, *args, **kwargs):
        
        def destroy_queues():
            for q in self._queues:
                with q.mutex:
                    q.queue.clear()
                    
        destroy_queues()
        self.destroy_actors()
        self.apply_world_settings(self.og_settings)

    def _retrieve_data(self, sensor_queue, timeout):
        while True:
            data = sensor_queue.get(timeout=timeout)
            if data.frame == self.frame:
                return data

    
