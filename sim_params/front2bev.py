from sim_params.sensors.front2bev import sensors
from dan.utils import dict2obj

reload_map = True
map = 'Town01'
map_config = 'layers_all'

test_id = 'debug'
output_path = f"_dataset"

ego = {
    'bp': 'charger_2020',
    'sensors': sensors,
    'autopilot': True,
    'speed': -15.0,
}

traffic = {
    'spawn_traffic': False,
    'tm_port': 8000,
    'tm_hybrid': False,

    'n_vehicles': 50,
    'filterv': 'vehicle.*',
    'vehicle_speed': -20.0,

    'n_walkers': 100,
    'filterw': 'walker.pedestrian.*',
    'percent_running': 0.1,
    'percent_crossing': 0.1,
}

args = {
    "seed": 35,
    "test_id": test_id,
    "output_path": output_path,

    'reload_map': reload_map,
    'map': map,
    'map_config': map_config,

    'ego': ego,
    'traffic': traffic,

    'grid_size': [1,1],
    'window_size': (1024, 1024),

    'frames': -1,
}    

sim_args = dict2obj(args)
