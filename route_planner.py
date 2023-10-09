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
    a = carla.Location(a[0], a[1], a[2])
    b = carla.Location(b[0], b[1], b[2])

    sampling_resolution = 5
    grp = GlobalRoutePlanner(map, sampling_resolution)
    w1 = grp.trace_route(a, b)
    i = 0

    for w in w1:
        if i % 10 == 0:
            world.debug.draw_string(w[0].transform.location, 'o', draw_shadow=False,
            color=carla.Color(r=255, g=0, b=0), life_time=20.0,
            persistent_lines=False)
        else:
            world.debug.draw_string(w[0].transform.location, 'o', draw_shadow=False,
            color = carla.Color(r=0, g=0, b=255), life_time=20.0,
            persistent_lines=False)
        i += 1
        time.sleep(0.05)
    return [w[0].transform.location.x, w[0].transform.location.y, w[0].transform.location.z]


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
def plot_points(point, id ,color=carla.Color(r=255, g=255, b=0)):
        world.debug.draw_string(point, str(id), draw_shadow=False,
                color=color, life_time=30.0,
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


world.debug.draw_string(origin, 'o', draw_shadow=False,
            color=carla.Color(r=255, g=0, b=0), life_time=20.0,
            persistent_lines=False)

waypoints = []
road_wps = map.get_topology()
i = 0
for road in road_wps:
    for point in road:
        point = point.transform.location
        if point not in waypoints:
        #    plot_points(point, i)
            waypoints.append(point)
            i += 1

wp_order = [69, 61, 71, 80, 66, 38, 51, 8, 36, 25, 85, 32, 16, 45, 67, 5, 28, 59, 75, 69]

route = []
for j in wp_order:
    aux = waypoints[j]
    route.append([aux.x, aux.y, aux.z])

route = np.array(route)
a = route[0]
for i, p in enumerate(route):
   # plot_points(carla.Location(p[0], p[1], p[2]),i)
   a = route_planner(map, a, p)

print(route)



'''

with open('route-0_town01.npy', 'wb') as f:
    np.save(f, route)

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






    
        



