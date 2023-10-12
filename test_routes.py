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
    sampling_resolution = 5
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
        time.sleep(0.01)
    return w[0].transform.location

# -------------------------------------------
def plot_points(point, id ,color=carla.Color(r=255, g=255, b=0)):
        world.debug.draw_string(point, str(id), draw_shadow=False,
                color=color, life_time=10.0,
                persistent_lines=False)
    
def are_same_point(point, point_list, tsh):

    point = np.array((point.x, point.y))
    
    for p in point_list:
        p = np.array((p.x, p.y))
        dist = np.linalg.norm(point - p)
        if dist < tsh:
            return True
    return False

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

reload_map, map_name = False, 'Town03_Opt'

world = load_map(reload_map, map_name)
map = world.get_map()
spawn_points = map.get_spawn_points()

ids = []
waypoints = []
road_wps = map.get_topology()
i = 0
for road in road_wps:
    point = road[0]
    id = point.id
    point = point.transform.location

    if not are_same_point(point, waypoints, 2):
        plot_points(point, i)
        waypoints.append(point)
        ids.append(id)
        i += 1
        
town_03_route_idx = [159, 169, 12, 281, 109, 257, 75, 33, 80, 0, 195, 153, 261, 135, 98, 156, 159, 169]

a = waypoints[159]

route = []
for i, wp_idx in enumerate(town_03_route_idx):
    aux = waypoints[wp_idx]
    if i == 0:
        z = 0.3
    else:
        z = 0.0
    route.append([aux.x, aux.y, z])
    route_planner(map, a, aux)
    a = aux

route = np.array(route)

with open(f'sim_params/routes/front2bev_town03.npy', 'wb') as f:
    np.save(f, route)


'''

'''

town_01_route_idx = [45, 63, 69, 78, 17, 39, 20, 36, 71, 75, 2, 33, 45, 63]
town_02_route_idx = [56, 32, 34, 26, 4, 51, 4, 21, 31, 42, 56, 16]






    
        



