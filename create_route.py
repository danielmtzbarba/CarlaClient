# -------------------------------------------
import carla
import numpy as np
from src.simulation.route_planner import RoutePlanner
# -------------------------------------------
def plot_points(world, point, id ,color=carla.Color(r=255, g=255, b=0)):
    world.debug.draw_string(point, str(id), draw_shadow=False,
                            color=color, life_time=10.0,
                            persistent_lines=False)

def draw_route(world, planner):

    i = 0
    ids, waypoints = [], []

    for point in planner.road_wps:
        if not are_same_point(point, waypoints, 2):
            plot_points(world, point, i)
            waypoints.append(point)
            i += 1

    return ids, waypoints
    
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

def save_route(route, route_name):
    route = np.array(route)
    save_path = f'src/routes/{route_name}.npy'
    with open(save_path, 'wb') as f:
        np.save(f, route)

def new_route(world, planner,  waypoints, seq):
    wp_start = seq[0]
    a = waypoints[wp_start]

    route = []
    for i, wp_idx in enumerate(seq):
        aux = waypoints[wp_idx]
        if i == 0:
            z = 0.3
        else:
            z = 0.0
        route.append([aux.x, aux.y, z])

        wps = planner.get_route_waypoints(a, aux)
        planner.draw_route(world, wps)

        a = aux
    return route

client = carla.Client("localhost", 2000)
client.set_timeout(10)

#town_01_route_idx = [45, 63, 69, 78, 17, 39, 20, 36, 71, 75, 2, 33, 45, 63]
#town_03_route_idx = [159, 169, 12, 281, 109, 257, 75, 33, 80, 0, 195, 153, 261, 135, 98, 156, 159, 169]
town_02_route_idx = [56, 32, 34, 26, 4, 51, 4, 21, 31, 42, 56, 16]

seq, n_seq = [27, 89], 1 

def main(map_name, reload, save):

    world = load_map(reload, f'{map_name}_Opt')
    planner = RoutePlanner(world, object, 2)
    planner.create_route(seq)
    draw_route(world, planner)
    if save:
        route_name =f'front2bev_{map_name}_seq_{n_seq}'
        save_route(planner.route, route_name)

if __name__ == '__main__':
    main(map_name='Town02', reload=False, save=False)
     
