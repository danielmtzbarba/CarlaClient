#!/usr/bin/env python

import carla

import logging
from numpy import random

SpawnActor = carla.command.SpawnActor
SetAutopilot = carla.command.SetAutopilot
FutureActor = carla.command.FutureActor

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

def change_traffic_light_timings(world):
    list_actor = world.get_actors()
    for actor_ in list_actor:
        if isinstance(actor_, carla.TrafficLight):
             # for any light, first set the light state, then set time. for yellow it is 
             # carla.TrafficLightState.Yellow and Red it is carla.TrafficLightState.Red
            actor_.set_state(carla.TrafficLightState.Green) 
            actor_.set_green_time(10000.0)
