from src.agents.navigation.global_route_planner import GlobalRoutePlanner

def route_planner(map, a, b):
    sampling_resolution = 2
    grp = GlobalRoutePlanner(map, sampling_resolution)
    waypoints = grp.trace_route(a, b)
    return [w[0] for w in waypoints]
