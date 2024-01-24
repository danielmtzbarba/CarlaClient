import carla
import random

class Pedestrian(object):
    def __init__(self, config):
        self._config = config
        self._actor = None
        self._controller = None
        self._speed = None

    def setup(self, world, spawn_point):
        self._bp, controller_bp = world.get_pedestrian_bps()

        if self._bp.has_attribute('is_invincible'):
            self._bp.set_attribute('is_invincible', 'false')
        
        if self._bp.has_attribute('speed'):
            p = random.random()
            if (p <= self._config.percent_static):
                # no speed
                walker_speed = 0.0

            if (p > self._config.percent_walking):
                # walking
                walker_speed = self._bp.get_attribute('speed').recommended_values[1]

            if (p >= self._config.percent_running):
                # running
                walker_speed = self._bp.get_attribute('speed').recommended_values[2]
        else:
            # no speed
            walker_speed = 0.0

        self._actor = world.spawn_actor(self._bp, spawn_point)    
        self._speed = walker_speed 

        return self

    @property   
    def location(self):
        return self._actor.get_location()

    @property
    def bp(self):
        return self._bp

    @property
    def actor(self):
        return self._actor
