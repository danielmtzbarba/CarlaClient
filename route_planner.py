import carla
import random
import time

from agents.navigation.global_route_planner import GlobalRoutePlanner

waypoints = []

def lane_waypoints(current_waypoint, dist):
    """
    Creates a new waypoint.
    """
    next_waypoint = current_waypoint.next_until_lane_end(dist)
    return next_waypoint

def route_planner(map, a, b):
    sampling_resolution = 20
    grp = GlobalRoutePlanner(map, sampling_resolution)
    w1 = grp.trace_route(a, b)
    i = 0

    for w in w1:
        if i % 10 == 0:
            world.debug.draw_string(w[0].transform.location, '.', draw_shadow=False,
            color=carla.Color(r=255, g=0, b=0), life_time=20.0,
            persistent_lines=False)
        else:
            world.debug.draw_string(w[0].transform.location, '.', draw_shadow=False,
            color = carla.Color(r=0, g=0, b=255), life_time=20.0,
            persistent_lines=False)
        i += 1


client = carla.Client("localhost", 2000)
client.set_timeout(10)

reload_map = False
if reload_map:
    world = client.load_world('Town01')
else:
    world = client.get_world()

map = world.get_map()
spawn_points = map.get_spawn_points()
# -------------------------------------------
def plot_points(point_list, color=carla.Color(r=255, g=255, b=0)):
    for i, point in enumerate(point_list):
        world.debug.draw_string(point, str(i), draw_shadow=False,
                color=color, life_time=10.0,
                persistent_lines=False)


def traverse_lane(waypoints_l, color=carla.Color(r=255, g=255, b=0)):

    for i, wp in enumerate(waypoints_l):
        if i == len(waypoints_l)-1:
            color =carla.Color(r=255, g=0, b=255)

        world.debug.draw_string(wp.transform.location, 'o', draw_shadow=False,
            color=color, life_time=20.0,
            persistent_lines=False)

    return current_waypoint

def advance(waypoint, n, dist):
    for _ in range(n):
        wp = waypoint.next(dist)[0]
        waypoint = wp
    return waypoint

# -------------------------------------------
# Spawn point

origin = carla.Location(0.0, 0.0, 0.0)
current_waypoint =  map.get_waypoint(origin)
waypoints.append(current_waypoint)

world.debug.draw_string(origin, 'o', draw_shadow=False,
            color=carla.Color(r=255, g=0, b=0), life_time=20.0,
            persistent_lines=False)

a = carla.Location(origin)
b = carla.Location(0.0, 325.0, 0.0)
c = carla.Location(395.0, 325.0, 0.0)
d = carla.Location(395.0, 0.0, 0.0)
e = carla.Location(340.0, 0.0, 0.0)
f = carla.Location(340.0, 324.0, 0.0)
g = carla.Location(93.0, 324.0, 0.0)
h = carla.Location(93.0, 130.0, 0.0) 
i = carla.Location(340.0, 130.0, 0.0)
j = carla.Location(340.0, 195.0, 0.0) 
k = carla.Location(90.0, 195.0, 0.0) 
l = carla.Location(90.0, 50.0, 0.0)
m = carla.Location(340.0, 50.0, 0.0)
n = carla.Location(340.0, 0.0, 0.0)
o = carla.Location(155.0, 0.0, 0.0)
p = carla.Location(155.0, 50.0, 0.0)
q = carla.Location(90.0, 50.0, 0.0)

r = carla.Location(90.0, 0.0, 0.0)
s = carla.Location(0.0, 0.0, 0.0)


plot_points([a, b, c, d, e, f, g, h, i,
             j, k, l, m, n, o, p, q, r,
             s, ])


'''
for points in range(n_points):
    current_waypoint = advance(current_waypoint, 5, dist)
    waypoints_l = current_waypoint.next_until_lane_end(dist)
    current_waypoint = traverse_lane(waypoints_l)
    waypoints_l = current_waypoint.previous_until_lane_start(dist)
    current_waypoint = traverse_lane(waypoints_l)


'''






    
        



