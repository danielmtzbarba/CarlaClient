#!/usr/bin/env python

# Copyright (c) 2021 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Example script to generate traffic in the simulation"""

import glob
import os
import sys
import time

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import logging
from numpy import random

from dan.utils import dict2obj

SpawnActor = carla.command.SpawnActor
SetAutopilot = carla.command.SetAutopilot
FutureActor = carla.command.FutureActor

traffic = {
    'seed': 42,
    'tm_port': 8000,
    'tm_hybrid': False,

    'n_vehicles': 50,
    'filterv': 'vehicle.*',
    'vehicle_speed': 30.0,

    'n_walkers': 50,
    'filterw': 'walker.pedestrian.*',
    'percent_running': 0.1,
    'percent_crossing': 0.1,
}

args = dict2obj(traffic)

def spawn_sync(client, batch):
    actor_id, success = None, False
    for response in client.apply_batch_sync(batch, True):
        if response.error:
            # Spawn failed on this location.
            pass
        else:
            actor_id = response.actor_id
            success = True
    return success, actor_id

def spawn_vehicles(args, client, bp_library, spawn_points):

    vehicle_bps = bp_library.filter(args.filterv)

    # Safe spawn
    vehicle_bps = [x for x in vehicle_bps if x.get_attribute('base_type') == 'car']

    vehicle_bps = sorted(vehicle_bps, key=lambda bp: bp.id)

    n_spawn_points = len(spawn_points)

    n_vehicles = args.n_vehicles

    if n_vehicles > n_spawn_points:
        msg = 'Requested %d vehicles, but could only find %d spawn points'
        logging.warning(msg, args.n_vehicles, n_spawn_points)
        n_vehicles = n_spawn_points
    
    vehicles_list = []

    n_spawned = 0
    while n_spawned < n_vehicles:
        spawn_point = random.choice(spawn_points)
        spawn_points.remove(spawn_point)

        vehicle_bp = random.choice(vehicle_bps)
        if vehicle_bp.has_attribute('color'):
            color = random.choice(vehicle_bp.get_attribute('color').recommended_values)
            vehicle_bp.set_attribute('color', color)
        if vehicle_bp.has_attribute('driver_id'):
            driver_id = random.choice(vehicle_bp.get_attribute('driver_id').recommended_values)
            vehicle_bp.set_attribute('driver_id', driver_id)
    
        vehicle_bp.set_attribute('role_name', 'autopilot')

        success, vehicle_id = spawn_sync(client,
                                          [SpawnActor(vehicle_bp, spawn_point)
                                           .then(SetAutopilot(FutureActor, True, args.tm_port))])
        # Successfully spawned
        if success:
            n_spawned += 1
            vehicles_list.append(vehicle_id)
            

    return vehicles_list

def spawn_walkers(args, client, world, bp_library):

    blueprintsWalkers = bp_library.filter(args.filterw)
    walker_controller_bp = bp_library.find('controller.ai.walker')

    walkers_ids= []
    walkers_speed = []
    controller_ids = []

    n_spawned = 0
    while n_spawned < args.n_walkers:
        # 1. Create a random spawn location
        spawn_point = carla.Transform()
        loc = world.get_random_location_from_navigation()
        if (loc != None):
            spawn_point.location = loc
            walker_bp = random.choice(blueprintsWalkers)
            # set as not invincible
            if walker_bp.has_attribute('is_invincible'):
                walker_bp.set_attribute('is_invincible', 'false')
            # set the max speed
            if walker_bp.has_attribute('speed'):
                if (random.random() > args.percent_running):
                    # walking
                    walker_speed = walker_bp.get_attribute('speed').recommended_values[1]
                else:
                    # running
                    walker_speed = walker_bp.get_attribute('speed').recommended_values[2]
            else:
                # no speed
                walker_speed = 0.0

            # 2. If location isValid spawn walker
            success, walker_id = spawn_sync(client, [SpawnActor(walker_bp, spawn_point)])

            # 3. If spawn succeeded spawn the respective walker controller
            if success:
                n_spawned += 1
                success, con_id = spawn_sync(client, [SpawnActor(walker_controller_bp,
                                                    carla.Transform(), walker_id)])
                
                # 4. Put together walkers and controllers id 
                if success:
                    walkers_ids.append(walker_id)
                    walkers_speed.append(walker_speed)
                    controller_ids.append(con_id)

            else: 
                # Spawn failed, try next location.
                continue
        
        else:
            # Inavlid spawn point, try next locaiton.
            continue
    
    walkers_list = world.get_actors(walkers_ids)
    controllers_list = world.get_actors(controller_ids)

    return walkers_list, walkers_speed, controllers_list

def main():
 
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    args.seed = args.seed if args.seed is not None else int(time.time())
    random.seed(args.seed)

    try:
        world = client.get_world()

        traffic_manager = client.get_trafficmanager(args.tm_port)
        traffic_manager.set_global_distance_to_leading_vehicle(2.5)

        if args.tm_hybrid:
            traffic_manager.set_hybrid_physics_mode(True)
            traffic_manager.set_hybrid_physics_radius(70.0)

        traffic_manager.set_random_device_seed(args.seed)
        world.set_pedestrians_seed(args.seed)

        settings = world.get_settings()
        traffic_manager.set_synchronous_mode(True)

        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05

        world.apply_settings(settings)

        # --------------------------------------

        bp_library = world.get_blueprint_library()
        map = world.get_map()
        spawn_points = map.get_spawn_points()
        
        # --------------
        # Spawn vehicles
        # --------------

        vehicles_list = spawn_vehicles(args, client,
                                        bp_library, spawn_points)

        # -------------
        # Spawn Walkers
        # -------------

        (walkers_list,
         walkers_speed,
         controller_list) = spawn_walkers(args, client, 
                                          world, bp_library)
        
        # Set percentage of pedestrians than can cross the road
        world.set_pedestrians_cross_factor(args.percent_crossing)

        # Initialize walkers controllers and set target to walk 
        for walker_controller, speed in zip(controller_list, walkers_speed):
            # start walker
            walker_controller.start()
            # set walk to random point
            walker_controller.go_to_location(world.get_random_location_from_navigation())
            # max speed
            walker_controller.set_max_speed(float(speed))

        # Example of how to use Traffic Manager parameters
        traffic_manager.global_percentage_speed_difference(args.vehicle_speed)

        print('Spawned %d vehicles and %d walkers, press Ctrl+C to exit.'
               % (len(vehicles_list), len(walkers_list)))

        while True:
            world.tick()
    
    finally:

        settings = world.get_settings()
        settings.synchronous_mode = False
        settings.no_rendering_mode = False
        settings.fixed_delta_seconds = None
        world.apply_settings(settings)

        print('\nDestroying %d vehicles' % len(vehicles_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_list])

        # Stop walker 
        for walker_controller in controller_list:
            walker_controller.stop()

        print('\nDestroying %d walkers' % len(walkers_list))
        client.apply_batch([carla.command.DestroyActor(x.id) for x in walkers_list])
        client.apply_batch([carla.command.DestroyActor(x.id) for x in controller_list])

        time.sleep(0.5)

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
