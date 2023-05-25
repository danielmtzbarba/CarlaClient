#!/usr/bin/env python

# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Script that render multiple sensors in the same pygame window

By default, it renders four cameras, one LiDAR and one Semantic LiDAR.
It can easily be configure for any different number of sensors. 
"""

import glob
import os
import sys

from utils.utils import create_path

TEST_NAME = "TEST_1"
test_path = create_path("_out", TEST_NAME)

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import argparse
import random
import time
import numpy as np


try:
    import pygame
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_q
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

from utils import DisplayManager, SensorManager
from utils.utils import CustomTimer

def run_simulation(args, client):
    """This function performed one test run using the args parameters
    and connecting to the carla client passed.
    """

    display_manager = None
    vehicle = None
    vehicle_list = []
    timer = CustomTimer()

    try:

        # Getting the world and
        world = client.get_world()

        obj_types = [carla.CityObjectLabel.Buildings, carla.CityObjectLabel.Fences,
                     carla.CityObjectLabel.Other, carla.CityObjectLabel.Vegetation, 
                     carla.CityObjectLabel.Poles, carla.CityObjectLabel.RoadLines,
                     carla.CityObjectLabel.TrafficSigns, carla.CityObjectLabel.Bridge,
                     carla.CityObjectLabel.Walls, carla.CityObjectLabel.Static,
                     carla.CityObjectLabel.Dynamic, carla.CityObjectLabel.RailTrack,
                     carla.CityObjectLabel.GuardRail]
        
        for obj_type in obj_types:      
            env_objs = world.get_environment_objects(obj_type)

            objects_to_toggle = {x.id for x in env_objs}
            # Toggle off
            world.enable_environment_objects(objects_to_toggle, False)

        original_settings = world.get_settings()

        if args.sync:
            traffic_manager = client.get_trafficmanager(8000)
            settings = world.get_settings()
            traffic_manager.set_synchronous_mode(True)
            settings.synchronous_mode = True
            settings.fixed_delta_seconds = 0.05
            world.apply_settings(settings)


        # Instanciating the vehicle to which we attached the sensors
        bp = world.get_blueprint_library().filter('charger_2020')[0]
        vehicle = world.spawn_actor(bp, random.choice(world.get_map().get_spawn_points()))
        traffic_manager.ignore_lights_percentage(vehicle, 100)
        tm_port = traffic_manager.get_port()

        vehicle.set_autopilot(True, tm_port)
        vehicle_list.append(vehicle)


        #
        #

        # Display Manager organize all the sensors an its display in a window
        # If can easily configure the grid and the total window size
        display_manager = DisplayManager(grid_size=[1, 1], window_size=[args.width, args.height])

        # Then, SensorManager can be used to spawn RGBCamera, LiDARs and SemanticLiDARs as needed
        # and assign each of them to a grid position, 
        SensorManager(world, display_manager, 'RGBCamera', carla.Transform(carla.Location(x=0, z=2.0), carla.Rotation(yaw=+00)), 
                      vehicle, {}, display_pos=[0, 0], save_dir = test_path,render_enabled=False)
        SensorManager(world, display_manager, 'LiDAR', carla.Transform(carla.Location(x=0, z=2.0)), 
                     vehicle, {'channels' : '1', 'range' : '100',  'points_per_second': '720',
                                'rotation_frequency': '20'}, display_pos=[0, 1], save_dir = test_path, render_enabled=False)
        SensorManager(world, display_manager, 'SemCamera', carla.Transform(carla.Location(x=0, z=32), carla.Rotation(yaw=+00, pitch=-90)), 
                      vehicle, {}, save_dir = test_path, display_pos=[0, 0])
        
        #Simulation loop
        call_exit = False
        time_init_sim = timer.time()
        while True:
            # Carla Tick
            if args.sync:
                world.tick()
            else:
                world.wait_for_tick()

            # Render received data
            display_manager.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    call_exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_q:
                        call_exit = True
                        break

            if call_exit:
                break

    finally:
        if display_manager:
            display_manager.destroy()

        client.apply_batch([carla.command.DestroyActor(x) for x in vehicle_list])

        world.apply_settings(original_settings)



def main():
    argparser = argparse.ArgumentParser(
        description='CARLA Sensor tutorial')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '--sync',
        action='store_true',
        help='Synchronous mode execution')
    argparser.add_argument(
        '--async',
        dest='sync',
        action='store_false',
        help='Asynchronous mode execution')
    argparser.set_defaults(sync=True)
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1024x1024',
        help='window resolution (default: 1280x720)')

    args = argparser.parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(5.0)

        run_simulation(args, client)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':

    main()
