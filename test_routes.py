import carla
import random
import time
import numpy as np

from agents.navigation.global_route_planner import GlobalRoutePlanner

waypoints = []

def lane_waypoints(current_waypoint, dist):
    """
    Creates a new waypoint.
    """
    next_waypoint = current_waypoint.next_until_lane_end(dist)
    return next_waypoint

def route_planner(map, a, b):
    sampling_resolution = 1
    grp = GlobalRoutePlanner(map, sampling_resolution)
    w1 = grp.trace_route(a, b)
    i = 0

    for w in w1:
        if i % 10 == 0:
            world.debug.draw_string(w[0].transform.location, 'o', draw_shadow=False,
            color=carla.Color(r=255, g=0, b=0), life_time=5.0,
            persistent_lines=False)
        else:
            world.debug.draw_string(w[0].transform.location, 'o', draw_shadow=False,
            color = carla.Color(r=0, g=0, b=255), life_time=5.0,
            persistent_lines=False)
        i += 1
        time.sleep(0.001)
    return w[0].transform.location

# -------------------------------------------
def plot_points(point, id ,color=carla.Color(r=255, g=255, b=0)):
        world.debug.draw_string(point, str(id), draw_shadow=False,
                color=color, life_time=30.0,
                persistent_lines=False)

# -------------------------------------------
def load_map(reload_map: bool, map_name: str):
    if reload_map:
        world = client.load_world(map_name)
    else:
        world = client.get_world()

        # Spawn point
        origin = carla.Location(0.0, 0.0, 0.0)

        world.debug.draw_string(origin, 'o', draw_shadow=False,
                    color=carla.Color(r=255, g=0, b=0), life_time=20.0,
                    persistent_lines=False)
    return world
# -------------------------------------------
client = carla.Client("localhost", 2000)
client.set_timeout(10)

reload_map, map_name = False, 'Town04_Opt'

world = load_map(reload_map, map_name)
map = world.get_map()
spawn_points = map.get_spawn_points()


waypoints = []
road_wps = map.get_topology()
i = 0
for road in road_wps:
    #for point in road:
        point = road[0]
        point = point.transform.location
        plot_points(point, i)
        waypoints.append(point)
        i += 1
        

town_04_route_idx = [351, 263, 299, 308, 318, 326, 185, 366, 115, 360, 404, 423,
                     334, 293, 342, ]
a = waypoints[351]

route = []
for i, wp_idx in enumerate(town_04_route_idx):
    aux = waypoints[wp_idx]
    if i == 0:
        z = 0.3
    else:
        z = 0.0
    route.append([aux.x, aux.y, z])
    route_planner(map, a, aux)
    a = aux

route = np.array(route)

with open(f'sim_params/routes/front2bev_town04.npy', 'wb') as f:
    np.save(f, route)


'''

'''

town_01_route_idx = [68, 62, 74, 77, 38, 51, 8, 42, 25, 85, 32, 16, 88, 6, 28, 59, 76, 68]
town_02_route_idx = [33, 27, 65, 47, 62, 68, 67, 6, 60, 48, 32, 33]

town_03_route_idx = [165, 238, 146, 145, 259, 280, 292, 66, 73, 91, 1, 154, 105, 234, 235, 203, 165, 160]





    
        



